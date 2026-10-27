package com.liceomap.app

import androidx.activity.ComponentActivity
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.lifecycle.SavedStateHandle
import com.liceomap.app.data.repository.AnnouncementsRepository
import com.liceomap.app.data.repository.AuthenticationRepository
import com.liceomap.app.data.repository.ScheduleRepository
import com.liceomap.app.model.*
import com.liceomap.app.ui.content.SchoolContentViewModel
import com.liceomap.app.ui.navigation.AppNavigation
import com.liceomap.app.ui.navigation.AppViewModel
import org.junit.Assert.*
import org.junit.Before
import org.junit.Rule
import org.junit.Test

/** Both access paths use in-memory repositories: no API, MariaDB or real accounts. */
class SchoolMapFlowTest {
    @get:Rule val rule = createAndroidComposeRule<ComponentActivity>()

    @Before fun showAppWithIsolatedRepositories() {
        val authentication = object : AuthenticationRepository {
            override suspend fun authenticate(rut: String, password: String) =
                AuthenticationResult.Authenticated(AuthenticatedUser("map-test-user", "1F"))
        }
        val schedules = object : ScheduleRepository {
            override suspend fun loadSchedule(course: String) = Schedule(course, emptyList())
        }
        val announcements = object : AnnouncementsRepository {
            override suspend fun loadAnnouncements() = emptyList<Announcement>()
        }
        val app = AppViewModel(SavedStateHandle(), authentication)
        val content = SchoolContentViewModel(
            schedules = schedules,
            announcements = announcements,
            remoteSchedules = schedules,
            remoteAnnouncements = announcements,
        )
        rule.runOnUiThread {
            rule.activity.viewModelStore.put("map-test-app", app)
            rule.activity.viewModelStore.put("map-test-content", content)
        }
        rule.setContent { AppNavigation(app, content) }
    }

    private fun awaitMap() {
        rule.waitUntil(15_000) {
            rule.onAllNodesWithTag("school-map").fetchSemanticsNodes().isNotEmpty()
        }
        rule.onNodeWithTag("school-map").assertIsDisplayed()
        rule.onNodeWithText("Mapa no disponible").assertDoesNotExist()
        rule.onNodeWithText("Mapa del liceo").assertIsDisplayed()
    }

    @Test fun demoLoadsBundledMapAndAllowsZoomPanAndReset() {
        rule.onNodeWithTag("enter-demo").performClick()
        rule.onNodeWithTag("nav-MAP").performClick()
        awaitMap()
        rule.onNodeWithTag("school-map").assert(SemanticsMatcher.expectValue(
            androidx.compose.ui.semantics.SemanticsProperties.StateDescription, "Zoom 100%"))
        rule.onNodeWithTag("map-zoom-in").performClick()
        rule.onNodeWithTag("school-map").assert(SemanticsMatcher.expectValue(
            androidx.compose.ui.semantics.SemanticsProperties.StateDescription, "Zoom 150%"))
        rule.onNodeWithTag("school-map").performTouchInput { swipeLeft() }
        rule.onNodeWithTag("map-zoom-out").performClick()
        rule.onNodeWithTag("map-reset").performClick()
        rule.onNodeWithTag("school-map").assert(SemanticsMatcher.expectValue(
            androidx.compose.ui.semantics.SemanticsProperties.StateDescription, "Zoom 100%"))
    }

    @Test fun authenticatedSessionLoadsTheSameMapWithoutDemoFallback() {
        rule.onNodeWithTag("rut-input").performScrollTo().performTextReplacement("20100001-7")
        rule.onNodeWithTag("password-input").performScrollTo().performTextReplacement("test-only")
        rule.onNodeWithTag("login-submit").performScrollTo().performClick()
        rule.onNodeWithText("Tu día en LiceoMap").assertIsDisplayed()
        rule.onNodeWithTag("nav-MAP").performClick()
        awaitMap()
        rule.onNodeWithText("Mapa en desarrollo").assertDoesNotExist()
        rule.onNodeWithTag("nav-HOME").performClick()
        rule.onNodeWithText("Tu día en LiceoMap").assertIsDisplayed()
    }
}
