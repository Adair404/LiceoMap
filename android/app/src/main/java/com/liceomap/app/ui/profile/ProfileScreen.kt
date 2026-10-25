package com.liceomap.app.ui.profile

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp
import com.liceomap.app.model.SchoolSession
import com.liceomap.app.model.AuthenticatedUser
import com.liceomap.app.ui.components.*
import com.liceomap.app.ui.theme.ThemeMode

@Composable
fun ProfileScreen(session: SchoolSession, mode: ThemeMode, version: String, onThemeChanged: (ThemeMode) -> Unit, onLogout: () -> Unit) {
    var confirmLogout by rememberSaveable { mutableStateOf(false) }
    LazyColumn(modifier = Modifier.testTag("profile-list"), contentPadding = PaddingValues(20.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        item { Text("Tu espacio", style = MaterialTheme.typography.headlineLarge) }
        item {
            SchoolCard {
                Text(session.studentName ?: "Estudiante de demostración", style = MaterialTheme.typography.titleLarge)
                Text(session.course)
                if (session.isDemo) {
                    DemoNotice()
                    Text("Esta sesión es local y no acredita una identidad del colegio.")
                } else Text("Rol: ${(session as? AuthenticatedUser)?.role.orEmpty()}")
            }
        }
        item {
            SchoolCard {
                Text("A tu manera", style = MaterialTheme.typography.titleLarge)
                Text("Apariencia")
                ThemeMode.entries.forEach { theme ->
                    Row(Modifier.fillMaxWidth(), verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
                        RadioButton(selected = mode == theme, onClick = { onThemeChanged(theme) },
                            modifier = Modifier.testTag("theme-${theme.name}"))
                        TextButton(onClick = { onThemeChanged(theme) }) { Text(theme.label) }
                    }
                }
            }
        }
        item { Text("LiceoMap · Versión $version", style = MaterialTheme.typography.bodyMedium) }
        item {
            OutlinedButton(onClick = { confirmLogout = true }, modifier = Modifier.fillMaxWidth().testTag("logout")) {
                Text("Cerrar sesión")
            }
        }
    }
    if (confirmLogout) AlertDialog(
        onDismissRequest = { confirmLogout = false },
        title = { Text(if (session.isDemo) "¿Cerrar la sesión de demostración?" else "¿Cerrar sesión?") },
        text = { Text(if (session.isDemo) "Podrás volver a explorar la aplicación desde el inicio."
            else "Para volver a entrar necesitarás tu cuenta.") },
        confirmButton = { TextButton(onClick = { confirmLogout = false; onLogout() },
            modifier = Modifier.testTag("confirm-logout")) { Text("Cerrar sesión") } },
        dismissButton = { TextButton(onClick = { confirmLogout = false }) { Text("Cancelar") } },
    )
}
