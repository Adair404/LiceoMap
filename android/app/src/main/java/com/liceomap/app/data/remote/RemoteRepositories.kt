package com.liceomap.app.data.remote

import com.liceomap.app.data.repository.*
import com.liceomap.app.model.*
import kotlinx.coroutines.CancellationException
import retrofit2.HttpException
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.Locale

class RemoteAuthenticationRepository(private val client: RemoteClient = RemoteServices.client) : AuthenticationRepository {
    override suspend fun authenticate(rut: String, password: String): AuthenticationResult {
        val attempt = client.session.begin()
        return try {
            val login = client.api.login(LoginBody(rut,password))
            client.session.accept(login.access_token,login.expires_in,attempt)
            val user = client.api.me().toUser()
            client.session.identify(user,attempt)
            AuthenticationResult.Authenticated(user)
        } catch (cancelled: CancellationException) { client.session.cancel(attempt); throw cancelled
        } catch (error: Exception) {
            client.session.cancel(attempt)
            AuthenticationResult.Rejected(when (error) {
                is HttpException -> when (error.code()) {
                    401 -> "RUT o contraseña incorrectos."
                    429 -> "Demasiados intentos. Espera unos minutos."
                    422 -> "Revisa el RUT y la contraseña."
                    else -> "El servicio no está disponible. Intenta nuevamente."
                }
                is IOException -> "No se pudo conectar con el servidor. Revisa tu conexión."
                else -> "No se pudo iniciar sesión. Intenta nuevamente."
            })
        }
    }
    override suspend fun logout() {
        val token = client.session.token()
        client.session.clear()
        if (token != null) try { client.api.logout("Bearer $token")
        } catch (cancelled: CancellationException) { throw cancelled
        } catch (_: Exception) { /* Local session is already erased. Server session expires. */ }
    }
}

class RemoteAnnouncementsRepository(private val client: RemoteClient = RemoteServices.client) : AnnouncementsRepository {
    override suspend fun loadAnnouncements(): List<Announcement> = client.api.announcements().map {
        val format = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ssXXX",Locale.ROOT).apply { isLenient = false }
        Announcement(it.id_anuncio.toString(),it.titulo,it.contenido,it.prioridad,
            requireNotNull(format.parse(it.fecha_publicacion)).time)
    }
}

class RemoteScheduleRepository(private val client: RemoteClient = RemoteServices.client) : ScheduleRepository {
    override suspend fun loadSchedule(course: String): Schedule {
        require(course.isNotBlank()) { "No hay curso asignado" }
        return Schedule(course,client.api.schedule(course).map {
            Lesson(it.dia_semana,it.hora_inicio.take(5),it.hora_fin.take(5),it.materia,it.espacio,RoomId(it.id_espacio))
        })
    }
}
