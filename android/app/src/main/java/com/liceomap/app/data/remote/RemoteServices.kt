package com.liceomap.app.data.remote

import com.liceomap.app.BuildConfig
import com.liceomap.app.model.AuthenticatedUser
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*
import java.util.concurrent.TimeUnit

/** Process memory only: never serialized, logged, backed up, or saved in SavedStateHandle. */
class MemorySession {
    @Volatile private var bearer: String? = null
    @Volatile var version: Long = 0; private set
    private val mutableUser = MutableStateFlow<AuthenticatedUser?>(null)
    val user = mutableUser.asStateFlow()
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
    private var expiry: Job? = null
    fun token(): String? = bearer
    @Synchronized fun clear() {
        version++; bearer = null; mutableUser.value = null; expiry?.cancel(); expiry = null
    }
    @Synchronized fun begin(): Long { clear(); return version }
    @Synchronized fun accept(token: String, seconds: Long, attempt: Long) {
        check(version == attempt)
        require(token.isNotBlank() && seconds in 1..28800)
        bearer = token
        expiry = scope.launch { delay(seconds * 1000); invalidate(token) }
    }
    @Synchronized fun identify(user: AuthenticatedUser, attempt: Long) {
        check(version == attempt && bearer != null); mutableUser.value = user
    }
    @Synchronized fun invalidate(token: String) { if (bearer == token) clear() }
    @Synchronized fun cancel(attempt: Long) { if (version == attempt) clear() }
}

// Deliberately regular classes: generated toString() must never print passwords or tokens.
class LoginBody(val rut: String, val password: String)
class LoginResponse(val access_token: String, val expires_in: Long)
data class CourseDto(val id_curso: String, val nombre: String)
data class UserDto(val id_usuario: Int, val nombre: String, val apellido: String, val rol: String,
                   val cursos: List<CourseDto>) {
    fun toUser() = AuthenticatedUser(id_usuario.toString(), cursos.firstOrNull()?.id_curso ?: "",
        "$nombre $apellido", rol, cursos.map { it.id_curso })
}
data class AnnouncementDto(val id_anuncio: Int, val titulo: String, val contenido: String,
                           val prioridad: String, val fecha_publicacion: String)
data class LessonDto(val dia_semana: Int, val hora_inicio: String, val hora_fin: String,
                     val materia: String, val espacio: String, val id_espacio: String)

interface LiceoMapApi {
    @POST("auth/login") suspend fun login(@Body body: LoginBody): LoginResponse
    @GET("me") suspend fun me(): UserDto
    @POST("auth/logout") suspend fun logout(@Header("Authorization") authorization: String)
    @GET("anuncios") suspend fun announcements(): List<AnnouncementDto>
    @GET("cursos/{id}/horarios") suspend fun schedule(@Path("id") course: String): List<LessonDto>
}

class RemoteClient(val session: MemorySession, baseUrl: String = BuildConfig.API_BASE_URL) {
    val api: LiceoMapApi
    init {
        val uri = java.net.URI(baseUrl)
        require(uri.scheme == "https" || (BuildConfig.DEBUG && uri.scheme == "http" &&
            uri.host in listOf("10.0.2.2", "127.0.0.1", "localhost"))) { "API requires HTTPS or a local DEBUG destination" }
        require(uri.userInfo == null && uri.query == null && uri.fragment == null && baseUrl.endsWith('/'))
        val http = OkHttpClient.Builder().connectTimeout(5, TimeUnit.SECONDS).readTimeout(10, TimeUnit.SECONDS)
            .callTimeout(15, TimeUnit.SECONDS).followRedirects(false).followSslRedirects(false)
            .addInterceptor { chain ->
                val token = session.token()
                val request = chain.request().newBuilder().header("Accept", "application/json")
                if (token != null && chain.request().header("Authorization") == null) request.header("Authorization", "Bearer $token")
                val response = chain.proceed(request.build())
                if (response.code == 401 && token != null) session.invalidate(token)
                response
            }.build()
        api = Retrofit.Builder().baseUrl(baseUrl).client(http).addConverterFactory(GsonConverterFactory.create())
            .build().create(LiceoMapApi::class.java)
    }
}

object RemoteServices {
    val session = MemorySession()
    val client by lazy { RemoteClient(session) }
}
