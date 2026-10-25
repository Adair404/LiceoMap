package com.liceomap.app.data.remote

import com.liceomap.app.model.*
import kotlinx.coroutines.*
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import org.junit.*
import org.junit.Assert.*

class RemoteRepositoriesTest {
    private lateinit var server: MockWebServer
    private lateinit var session: MemorySession
    private lateinit var client: RemoteClient
    private val me = """{"id_usuario":4,"nombre":"Estudiante","apellido":"Prueba","rol":"alumno","cursos":[{"id_curso":"1F","nombre":"1 Medio F"}]}"""
    @Before fun setup() {
        server = MockWebServer(); server.start()
        session = MemorySession(); client = RemoteClient(session,server.url("/").toString())
    }
    @After fun close() { session.clear(); server.shutdown() }
    private fun respond(body: String, code: Int = 200) { server.enqueue(MockResponse().setResponseCode(code).setBody(body)) }
    private fun install() { val attempt = session.begin(); session.accept("test-bearer",60,attempt) }

    @Test fun loginChecksMeAndOnlyThenExposesIdentity() = runBlocking {
        respond("""{"access_token":"test-bearer","expires_in":60}"""); respond(me)
        val result = RemoteAuthenticationRepository(client).authenticate("20100006-8","transient-password")
        assertTrue(result is AuthenticationResult.Authenticated)
        assertEquals("1F",session.user.value?.course)
        assertFalse(session.user.value!!.isDemo)
        assertEquals("/auth/login",server.takeRequest().path)
        assertEquals("Bearer test-bearer",server.takeRequest().getHeader("Authorization"))
    }
    @Test fun deniedMeClearsPendingBearerAndIdentity() = runBlocking {
        respond("""{"access_token":"test-bearer","expires_in":60}"""); respond("{}",401)
        assertTrue(RemoteAuthenticationRepository(client).authenticate("20100006-8","x") is AuthenticationResult.Rejected)
        assertNull(session.token()); assertNull(session.user.value)
    }
    @Test fun invalidLoginHasSafeMessage() = runBlocking {
        respond("""{"detail":"internal SQL should not appear"}""",401)
        val result = RemoteAuthenticationRepository(client).authenticate("20100006-8","x") as AuthenticationResult.Rejected
        assertEquals("RUT o contraseña incorrectos.",result.message); assertNull(session.token())
    }
    @Test fun announcementsUseServerAndUtcDateAndReloadWithoutCache() = runBlocking {
        install()
        respond("""[{"id_anuncio":42,"titulo":"Uno","contenido":"Servidor","prioridad":"URGENTE","fecha_publicacion":"2026-10-24T12:00:00+00:00"}]""")
        respond("[]")
        val repo = RemoteAnnouncementsRepository(client)
        val first = repo.loadAnnouncements().single()
        assertEquals("42",first.id); assertTrue(first.publishedAt > 0); assertEquals("URGENTE",first.category)
        assertTrue(repo.loadAnnouncements().isEmpty())
        repeat(2) { assertEquals("Bearer test-bearer",server.takeRequest().getHeader("Authorization")) }
    }
    @Test fun unauthorizedContentClearsSession() = runBlocking {
        install(); respond("{}",401)
        try { RemoteAnnouncementsRepository(client).loadAnnouncements(); fail("Expected unauthorized")
        } catch (_: retrofit2.HttpException) { }
        assertNull(session.token())
    }
    @Test fun serverErrorCanRecoverWithoutDemoFallback() = runBlocking {
        install(); respond("{}",503); respond("[]")
        val repo = RemoteAnnouncementsRepository(client)
        try { repo.loadAnnouncements(); fail("Expected service error") } catch (_: retrofit2.HttpException) { }
        assertNotNull(session.token()); assertTrue(repo.loadAnnouncements().isEmpty())
    }
    @Test fun logoutClearsMemoryAndRevokesServerSession() = runBlocking {
        install(); server.enqueue(MockResponse().setResponseCode(204))
        RemoteAuthenticationRepository(client).logout()
        assertNull(session.token()); assertNull(session.user.value)
        assertEquals("Bearer test-bearer",server.takeRequest().getHeader("Authorization"))
    }
    @Test fun expiredSessionAndLateResponsesCannotReinstallIdentity() = runBlocking {
        val attempt = session.begin(); session.accept("short-lived",1,attempt)
        delay(1200); assertNull(session.token())
        try { session.identify(AuthenticatedUser("4","1F"),attempt); fail("Late identity") } catch (_: IllegalStateException) { }
    }
    @Test fun releaseStyleClientRejectsArbitraryCleartextHosts() {
        try { RemoteClient(session,"http://192.168.1.4:8000/"); fail("Nonlocal cleartext accepted")
        } catch (_: IllegalArgumentException) { }
    }
}
