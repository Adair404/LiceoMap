package com.liceomap.app.model

data class AuthenticatedUser(val id: String, override val course: String,
    override val studentName: String? = null, val role: String = "alumno",
    val courses: List<String> = listOf(course)) : SchoolSession {
    override val isDemo = false
}

sealed interface AuthenticationResult {
    data class Authenticated(val user: AuthenticatedUser) : AuthenticationResult
    data class Rejected(val message: String) : AuthenticationResult
}
