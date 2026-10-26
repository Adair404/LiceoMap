package com.liceomap.app

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.*
import java.io.File
import java.net.HttpURLConnection
import java.net.URL

/** Credentials arrive as ephemeral instrumentation arguments, never in the APK. */
class PreoficialSyncTest {
    @get:Rule val rule = createAndroidComposeRule<MainActivity>()
    private val args get() = InstrumentationRegistry.getArguments()
    private val files get() = InstrumentationRegistry.getInstrumentation().targetContext.filesDir
    private fun control(name: String, method: String): Boolean {
        val conn = URL("http://127.0.0.1:5502/control/$name").openConnection() as HttpURLConnection
        conn.requestMethod = method; conn.connectTimeout = 3000; conn.readTimeout = 3000
        return try { conn.responseCode == 200 } finally { conn.disconnect() }
    }
    private fun signal(name: String) { Assert.assertTrue(control(name,"POST")) }
    private fun await(name: String) {
        val deadline = System.currentTimeMillis()+120000
        while (!control(name,"GET")) { Assert.assertTrue("Waiting for $name",System.currentTimeMillis()<deadline); Thread.sleep(250) }
    }
    private fun textAppears(text: String) {
        rule.waitUntil(30000) { rule.onAllNodesWithText(text).fetchSemanticsNodes().isNotEmpty() }
    }
    private fun refresh() {
        rule.onNodeWithTag("announcements-list").performScrollToIndex(0)
        rule.onNodeWithTag("refresh-announcements").performScrollTo().performClick()
    }
    private fun login() {
        rule.onNodeWithTag("rut-input").performScrollTo().performTextReplacement(requireNotNull(args.getString("rut")))
        rule.onNodeWithTag("password-input").performScrollTo().performTextReplacement(requireNotNull(args.getString("password")))
        rule.onNodeWithTag("login-submit").performScrollTo().performClick()
        textAppears("Hola, Jorge Badani")
        rule.onNodeWithTag("nav-ANNOUNCEMENTS").performClick()
        textAppears("Actualizar anuncios")
    }
    @Test fun webPublicationRefreshEditRecoveryWithdrawalExpirationAndLogout() {
        Assume.assumeTrue(args.getString("preoficial") == "true")
        Assert.assertEquals("http://127.0.0.1:8001/",BuildConfig.API_BASE_URL)
        files.listFiles()?.filter { it.name.startsWith("sync-") }?.forEach { it.delete() }
        val title = requireNotNull(args.getString("title"))
        login()
        rule.onAllNodesWithText("Datos de demostración",substring=true).assertCountEquals(0)
        signal("waiting-publication"); await("published")
        refresh(); textAppears(title)
        rule.activityRule.scenario.recreate()
        textAppears(title)
        signal("seen-publication"); await("edited")
        refresh(); textAppears(title+" editado")
        signal("seen-edit"); await("offline")
        refresh(); textAppears("No pudimos cargar los anuncios")
        signal("seen-offline"); await("online")
        refresh(); textAppears(title+" editado")
        signal("seen-recovery"); await("withdrawn")
        refresh()
        rule.waitUntil(30000) {
            rule.onAllNodesWithText(title+" editado").fetchSemanticsNodes().isEmpty() &&
                rule.onAllNodesWithText("Buscando novedades…").fetchSemanticsNodes().isEmpty()
        }
        signal("seen-withdrawal"); await("expired")
        refresh(); textAppears("Acceso institucional")
        signal("seen-expiry")
        login()
        rule.onNodeWithTag("nav-PROFILE").performClick()
        rule.onNodeWithTag("logout").performScrollTo().performClick()
        rule.onNodeWithTag("confirm-logout").performClick()
        rule.onNodeWithTag("enter-demo").assertIsDisplayed()
        signal("complete")
    }
}
