package com.liceomap.app.ui.content

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.liceomap.app.data.demo.*
import com.liceomap.app.data.remote.*
import com.liceomap.app.data.repository.*
import com.liceomap.app.model.*
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

data class SchoolContentState(
    val schedule: LoadState<Schedule> = LoadState.Loading,
    val announcements: LoadState<List<Announcement>> = LoadState.Loading,
)

/** One owner; authenticated requests never fall back to presentation content. */
class SchoolContentViewModel(
    private val schedules: ScheduleRepository = DemoScheduleRepository(),
    private val announcements: AnnouncementsRepository = DemoAnnouncementsRepository(),
    private val dispatcher: CoroutineDispatcher = Dispatchers.Main.immediate,
    private val remoteSchedules: ScheduleRepository = RemoteScheduleRepository(),
    private val remoteAnnouncements: AnnouncementsRepository = RemoteAnnouncementsRepository(),
) : ViewModel() {
    private val mutableState = MutableStateFlow(SchoolContentState())
    val uiState = mutableState.asStateFlow()
    private var scheduleJob: Job? = null
    private var announcementsJob: Job? = null
    private var remote = false
    private var generation = 0L
    private var announcementVersion = 0L

    fun clear() {
        generation++; announcementVersion++
        scheduleJob?.cancel(); announcementsJob?.cancel()
        mutableState.value = SchoolContentState()
    }

    fun load(course: String, authenticated: Boolean = false) {
        clear(); remote = authenticated
        val version = generation
        val repository = if (remote) remoteSchedules else schedules
        scheduleJob = viewModelScope.launch(dispatcher) {
            try {
                val data = repository.loadSchedule(course)
                require(data.course == course) { "Schedule belongs to another course" }
                if (version == generation) mutableState.update { it.copy(schedule = LoadState.Ready(data)) }
            } catch (cancelled: CancellationException) { throw cancelled
            } catch (_: Exception) {
                if (version == generation) mutableState.update { it.copy(schedule = LoadState.Error(
                    if (course.isBlank()) "No tienes curso asignado." else "No pudimos cargar el horario. Revisa tu conexión.")) }
            }
        }
        refreshAnnouncements()
    }

    fun refreshAnnouncements() {
        announcementsJob?.cancel()
        val version = ++announcementVersion
        val session = generation
        val repository = if (remote) remoteAnnouncements else announcements
        mutableState.update { it.copy(announcements = LoadState.Loading) }
        announcementsJob = viewModelScope.launch(dispatcher) {
            try {
                val items = repository.loadAnnouncements()
                require(items.map { it.id }.distinct().size == items.size) { "Duplicate announcement identities" }
                val data = items.sortedWith(compareByDescending<Announcement> { it.publishedAt }.thenBy { it.id })
                if (version == announcementVersion && session == generation)
                    mutableState.update { it.copy(announcements = LoadState.Ready(data)) }
            } catch (cancelled: CancellationException) { throw cancelled
            } catch (_: Exception) {
                if (version == announcementVersion && session == generation)
                    mutableState.update { it.copy(announcements = LoadState.Error("No pudimos cargar los anuncios. Revisa tu conexión y actualiza.")) }
            }
        }
    }
}
