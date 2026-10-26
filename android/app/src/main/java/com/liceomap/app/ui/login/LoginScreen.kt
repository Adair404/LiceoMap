package com.liceomap.app.ui.login

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.School
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import com.liceomap.app.domain.*
import com.liceomap.app.ui.components.SchoolCard

@Composable
fun LoginScreen(rut: String, onRutChanged: (String) -> Unit, onEnter: () -> Unit,
    onLogin: (String) -> Unit = {}, loading: Boolean = false, loginError: String? = null) {
    // Deliberately remember, not rememberSaveable: no password in saved instance state.
    var password by remember { mutableStateOf("") }
    val validation = ChileanRut.validate(rut)
    val error = when (validation) {
        RutValidation.InvalidFormat -> "Usa un RUT con guion, por ejemplo 12.345.678-5."
        RutValidation.InvalidCheckDigit -> "El dígito verificador no coincide."
        else -> null
    }
    Column(
        Modifier.fillMaxSize().windowInsetsPadding(WindowInsets.safeDrawing).imePadding()
            .verticalScroll(rememberScrollState()).padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(24.dp, Alignment.CenterVertically),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Icon(Icons.Default.School, contentDescription = null, modifier = Modifier.size(56.dp),
            tint = MaterialTheme.colorScheme.primary)
        Text("LiceoMap", style = MaterialTheme.typography.headlineLarge)
        Text("Tu colegio, más cerca.", style = MaterialTheme.typography.titleMedium)
        SchoolCard {
            Text("Conoce tu próximo día", style = MaterialTheme.typography.titleLarge)
            Text("Explora horarios, salas y anuncios de ejemplo. El modo demostración no requiere RUT ni contraseña.")
            Button(onClick = onEnter, enabled = !loading, modifier = Modifier.fillMaxWidth().testTag("enter-demo")) {
                Text("Explorar demostración")
            }
        }
        SchoolCard {
            Text("Acceso institucional", style = MaterialTheme.typography.titleMedium)
            Text("Inicia sesión con tu cuenta. Versión preliminar.")
            OutlinedTextField(
                value = rut, onValueChange = onRutChanged, singleLine = true,
                label = { Text("RUT") },
                supportingText = {
                    Text(error ?: if (validation is RutValidation.Valid) "Formato y dígito verificador válidos."
                        else "Ingresa el RUT de tu cuenta.")
                },
                isError = error != null, keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Ascii),
                modifier = Modifier.fillMaxWidth().testTag("rut-input"),
            )
            OutlinedTextField(value = password, onValueChange = { password = it }, singleLine = true,
                label = { Text("Contraseña") }, visualTransformation = PasswordVisualTransformation(),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                enabled = !loading, modifier = Modifier.fillMaxWidth().testTag("password-input"))
            if (loginError != null) Text(loginError, color = MaterialTheme.colorScheme.error,
                modifier = Modifier.testTag("login-error"))
            Button(onClick = { val entered = password; password = ""; onLogin(entered) },
                enabled = !loading && password.isNotBlank() && validation is RutValidation.Valid,
                modifier = Modifier.fillMaxWidth().testTag("login-submit")) {
                Text(if (loading) "Iniciando sesión…" else "Iniciar sesión")
            }
        }
    }
}
