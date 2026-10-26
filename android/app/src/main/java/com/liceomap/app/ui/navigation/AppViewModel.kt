package com.liceomap.app.ui.navigation

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.liceomap.app.data.remote.RemoteServices
import com.liceomap.app.data.remote.RemoteAuthenticationRepository
import com.liceomap.app.data.repository.AuthenticationRepository
import kotlinx.coroutines.launch
import kotlinx.coroutines.CoroutineStart
import com.liceomap.app.data.demo.DemoEntry
import com.liceomap.app.domain.*
import com.liceomap.app.model.*
import com.liceomap.app.ui.theme.ThemeMode
import kotlinx.coroutines.flow.*

class AppViewModel @JvmOverloads constructor(private val savedStateHandle: SavedStateHandle,
    private val authentication: AuthenticationRepository = RemoteAuthenticationRepository()) : ViewModel() {
    private fun restoredStack(): List<AppRoute> {
        val destinations = savedStateHandle.get<ArrayList<String>>("backDestinations") ?: return emptyList()
        val announcements = savedStateHandle.get<ArrayList<String>>("backAnnouncements") ?: return emptyList()
        val rooms = savedStateHandle.get<ArrayList<String>>("backRooms") ?: return emptyList()
        if (destinations.size != announcements.size || destinations.size != rooms.size) return emptyList()
        return destinations.mapIndexedNotNull { index, name ->
            val destination = AppDestination.entries.firstOrNull { it.name == name } ?: return@mapIndexedNotNull null
            AppRoute(destination,
                announcements[index].takeIf { destination == AppDestination.ANNOUNCEMENTS && it.isNotBlank() },
                rooms[index].takeIf { destination == AppDestination.MAP && it.isNotBlank() }?.let(::RoomId))
        }
    }
    private val mutableUiState = MutableStateFlow(
        AppUiState(
            rut = savedStateHandle["rut"] ?: "",
            demoSession = savedStateHandle.get<String>("demoCourse")?.takeIf { it.isNotBlank() }?.let {
                DemoSession(it, savedStateHandle["studentName"])
            },
            destination = AppDestination.entries.firstOrNull {
                it.name == savedStateHandle.get<String>("destination")
            } ?: AppDestination.HOME,
            selectedDay = savedStateHandle.get<Int>("selectedDay")?.takeIf { it in 1..7 }
                ?: ScheduleClock.dayOfWeek(System.currentTimeMillis()),
            selectedRoom = savedStateHandle.get<String>("selectedRoom")?.takeIf { it.isNotBlank() }?.let(::RoomId),
            announcementId = savedStateHandle["announcementId"],
            announcementCategory = savedStateHandle["announcementCategory"],
            announcementOrder = AnnouncementOrder.entries.firstOrNull {
                it.name == savedStateHandle.get<String>("announcementOrder")
            } ?: AnnouncementOrder.NEWEST,
            themeMode = ThemeMode.entries.firstOrNull {
                it.name == savedStateHandle.get<String>("themeMode")
            } ?: ThemeMode.SYSTEM,
            backStack = restoredStack(),
        )
    )
    val uiState = mutableUiState.asStateFlow()
    init {
        viewModelScope.launch {
            RemoteServices.session.user.collect { user ->
                if (user == null && uiState.value.authenticatedUser != null) {
                    clearLocalSession("La sesión terminó. Inicia sesión nuevamente.")
                } else if (user != null) {
                    savedStateHandle.remove<String>("demoCourse")
                    mutableUiState.update { it.copy(authenticatedUser = user, demoSession = null) }
                }
            }
        }
    }

    fun login(password: String) {
        if (uiState.value.authenticating) return
        val rut = (ChileanRut.validate(uiState.value.rut) as? RutValidation.Valid)?.normalized
        if (rut == null || password.isBlank() || password.toByteArray(Charsets.UTF_8).size > 72) {
            mutableUiState.update { it.copy(loginError = "Revisa tu RUT y contraseña (máximo 72 bytes).") }; return
        }
        mutableUiState.update { it.copy(authenticating = true, loginError = null) }
        viewModelScope.launch {
            when (val result = authentication.authenticate(rut,password)) {
                is AuthenticationResult.Authenticated -> {
                    mutableUiState.update { it.copy(authenticatedUser = result.user, demoSession = null, authenticating = false) }
                    setRoute(AppRoute(AppDestination.HOME),emptyList())
                }
                is AuthenticationResult.Rejected -> mutableUiState.update { it.copy(authenticating = false, loginError = result.message) }
            }
        }
    }

    private fun currentRoute() = uiState.value.let { AppRoute(it.destination, it.announcementId, it.selectedRoom) }

    private fun setRoute(route: AppRoute, stack: List<AppRoute>) {
        savedStateHandle["destination"] = route.destination.name
        savedStateHandle["announcementId"] = route.announcementId
        savedStateHandle["selectedRoom"] = route.room?.value
        savedStateHandle["backDestinations"] = ArrayList(stack.map { it.destination.name })
        savedStateHandle["backAnnouncements"] = ArrayList(stack.map { it.announcementId ?: "" })
        savedStateHandle["backRooms"] = ArrayList(stack.map { it.room?.value ?: "" })
        mutableUiState.update { it.copy(destination = route.destination, announcementId = route.announcementId,
            selectedRoom = route.room, backStack = stack) }
    }

    fun onRutChanged(rut: String) {
        savedStateHandle["rut"] = rut
        mutableUiState.update { it.copy(rut = rut) }
    }

    fun enterDemo(): DemoSession {
        RemoteServices.session.clear()
        val session = DemoEntry.enter()
        savedStateHandle["demoCourse"] = session.course
        savedStateHandle.remove<String>("rut")
        mutableUiState.update { it.copy(demoSession = session, authenticatedUser = null, rut = "", loginError = null) }
        setRoute(AppRoute(AppDestination.HOME), emptyList())
        return session
    }

    /** Main destinations replace the root; Schedule is a child of Home. */
    fun selectDestination(destination: AppDestination) {
        if (destination == AppDestination.SCHEDULE) {
            if (uiState.value.destination != destination) {
                setRoute(AppRoute(destination), uiState.value.backStack + currentRoute())
            }
        } else {
            setRoute(AppRoute(destination),
                if (destination == AppDestination.HOME) emptyList() else listOf(AppRoute(AppDestination.HOME)))
        }
    }

    fun selectDay(day: Int) {
        require(day in 1..7)
        savedStateHandle["selectedDay"] = day
        mutableUiState.update { it.copy(selectedDay = day) }
    }

    fun openRoom(room: RoomId) {
        setRoute(AppRoute(AppDestination.MAP, room = room), uiState.value.backStack + currentRoute())
    }

    fun openAnnouncement(id: String) {
        require(id.isNotBlank())
        if (uiState.value.destination != AppDestination.ANNOUNCEMENTS) selectDestination(AppDestination.ANNOUNCEMENTS)
        setRoute(AppRoute(AppDestination.ANNOUNCEMENTS, announcementId = id), uiState.value.backStack + currentRoute())
    }

    fun goBack(): Boolean {
        val stack = uiState.value.backStack
        if (stack.isEmpty()) return false
        setRoute(stack.last(), stack.dropLast(1))
        return true
    }

    fun closeAnnouncement() { if (uiState.value.announcementId != null) goBack() }

    fun selectCategory(category: String?) {
        savedStateHandle["announcementCategory"] = category
        mutableUiState.update { it.copy(announcementCategory = category) }
    }

    fun selectOrder(order: AnnouncementOrder) {
        savedStateHandle["announcementOrder"] = order.name
        mutableUiState.update { it.copy(announcementOrder = order) }
    }

    fun selectTheme(mode: ThemeMode) {
        savedStateHandle["themeMode"] = mode.name
        mutableUiState.update { it.copy(themeMode = mode) }
    }

    fun initializeTheme(mode: ThemeMode) {
        if (!savedStateHandle.contains("themeMode")) selectTheme(mode)
    }

    fun logout() {
        viewModelScope.launch(start = CoroutineStart.UNDISPATCHED) { authentication.logout() }
        clearLocalSession()
    }

    private fun clearLocalSession(message: String? = null) {
        val theme = uiState.value.themeMode
        savedStateHandle.keys().filter { it != "themeMode" }.forEach { savedStateHandle.remove<Any?>(it) }
        mutableUiState.value = AppUiState(themeMode = theme, loginError = message)
    }
}
