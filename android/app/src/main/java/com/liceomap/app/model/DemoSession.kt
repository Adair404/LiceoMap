package com.liceomap.app.model

/** Local demonstration access. This is never proof of an authenticated identity. */
interface SchoolSession {
    val course: String
    val studentName: String?
    val isDemo: Boolean
}

data class DemoSession(override val course: String, override val studentName: String? = null) : SchoolSession {
    override val isDemo = true
}
