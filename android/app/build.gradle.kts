import java.net.URI
import java.security.MessageDigest
import org.gradle.api.file.DirectoryProperty
import org.gradle.api.file.RegularFileProperty

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.compose)
}

val configuredApiUrl = providers.gradleProperty("liceomapApiBaseUrl").orNull?.also {
    val uri = URI(it)
    require(uri.scheme in listOf("http", "https") && uri.host != null && uri.userInfo == null &&
        uri.query == null && uri.fragment == null && it.endsWith('/') && !it.contains('"')) {
        "liceomapApiBaseUrl debe ser una URL sin credenciales, query ni fragmento, terminada en /"
    }
}

abstract class SyncSchoolMap : DefaultTask() {
    @get:InputFile
    @get:PathSensitive(PathSensitivity.RELATIVE)
    abstract val sourceSvg: RegularFileProperty

    @get:InputFile
    @get:PathSensitive(PathSensitivity.RELATIVE)
    abstract val sourcePng: RegularFileProperty

    @get:InputFile
    @get:PathSensitive(PathSensitivity.RELATIVE)
    abstract val sourceDigest: RegularFileProperty

    @get:OutputDirectory
    abstract val outputDirectory: DirectoryProperty

    @TaskAction
    fun copyMap() {
        val digest = MessageDigest.getInstance("SHA-256").digest(sourceSvg.get().asFile.readBytes())
            .joinToString("") { "%02x".format(it) }
        require(digest == sourceDigest.get().asFile.readText().trim()) {
            "El SVG cambió: ejecutar python3 scripts/render_android_map.py antes de compilar."
        }
        val output = outputDirectory.file("mapa_liceo_concepto.svg").get().asFile
        output.parentFile.mkdirs()
        sourceSvg.get().asFile.copyTo(output, overwrite = true)
        sourcePng.get().asFile.copyTo(outputDirectory.file("mapa_liceo_concepto.png").get().asFile, overwrite = true)
    }
}

// Package the canonical SVG unchanged; do not maintain a second editable copy.
val syncSchoolMap by tasks.registering(SyncSchoolMap::class) {
    sourceSvg.set(rootProject.file("../design/svg/mapa_liceo_concepto.svg"))
    sourcePng.set(rootProject.file("../design/android/mapa_liceo_concepto.png"))
    sourceDigest.set(rootProject.file("../design/android/mapa_liceo_concepto.svg.sha256"))
    outputDirectory.set(layout.buildDirectory.dir("generated/assets/schoolMap"))
}

android {
    namespace = "com.liceomap.app"
    compileSdk {
        version = release(37)
    }

    defaultConfig {
        applicationId = "com.liceomap.app"
        minSdk = 24
        targetSdk = 37
        versionCode = 2
        versionName = "0.2.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        buildConfigField("String", "API_BASE_URL", "\"${configuredApiUrl ?: "https://api.example.invalid/"}\"")
    }

    buildTypes {
        debug {
            buildConfigField("String", "API_BASE_URL", "\"${configuredApiUrl ?: "http://10.0.2.2:8000/"}\"")
        }
        release {
            optimization {
                enable = false
            }
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    buildFeatures {
        compose = true
        buildConfig = true
    }
}

androidComponents {
    onVariants(selector().all()) { variant ->
        variant.sources.assets?.addGeneratedSourceDirectory(syncSchoolMap, SyncSchoolMap::outputDirectory)
    }
}

dependencies {
    implementation("androidx.webkit:webkit:1.17.1")
    implementation("com.squareup.retrofit2:retrofit:2.11.0")
    implementation("com.squareup.retrofit2:converter-gson:2.11.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    testImplementation("com.squareup.okhttp3:mockwebserver:4.12.0")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.10.2")
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.activity.compose)
    implementation(libs.androidx.compose.material3)
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.ui.graphics)
    implementation(libs.androidx.compose.ui.tooling.preview)
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.lifecycle.runtime.compose)
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.lifecycle.viewmodel.savedstate)
    implementation("androidx.compose.material:material-icons-extended")
    testImplementation(libs.junit)
    testImplementation(libs.androidx.arch.core.testing)
    androidTestImplementation(platform(libs.androidx.compose.bom))
    androidTestImplementation(libs.androidx.compose.ui.test.junit4)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(libs.androidx.junit)
    debugImplementation(libs.androidx.compose.ui.test.manifest)
    debugImplementation(libs.androidx.compose.ui.tooling)
}
