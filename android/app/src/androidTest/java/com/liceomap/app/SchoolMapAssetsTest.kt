package com.liceomap.app

import android.net.Uri
import androidx.test.platform.app.InstrumentationRegistry
import com.liceomap.app.ui.map.MAP_PAGE_URL
import com.liceomap.app.ui.map.MAP_SVG_URL
import com.liceomap.app.ui.map.SchoolMapAssets
import org.junit.Assert.*
import org.junit.Test

class SchoolMapAssetsTest {
    private val context get() = InstrumentationRegistry.getInstrumentation().targetContext

    @Test fun httpsRoutesReturnPackagedHtmlAndOriginalSvgWithCorrectMimeTypes() {
        val loader = SchoolMapAssets(context)
        for ((url, asset, mime) in listOf(
            Triple(MAP_PAGE_URL, "mapa.html", "text/html"),
            Triple(MAP_SVG_URL, "mapa_liceo_concepto.svg", "image/svg+xml"),
        )) {
            val response = loader.intercept(Uri.parse(url))
            assertEquals(200, response.statusCode)
            assertEquals(mime, response.mimeType)
            assertEquals("UTF-8", response.encoding)
            assertEquals("no-store", response.responseHeaders?.get("Cache-Control"))
            val original = context.assets.open(asset).use { it.readBytes() }
            assertArrayEquals(original, requireNotNull(response.data).use { it.readBytes() })
        }
    }

    @Test fun otherOriginsSchemesAndAssetsAreRejectedWithoutNetworkFallback() {
        val loader = SchoolMapAssets(context)
        for (url in listOf(
            "https://example.invalid/mapa_liceo_concepto.svg",
            "http://appassets.androidplatform.net/assets/mapa.html",
            "file:///android_asset/mapa.html",
            "https://appassets.androidplatform.net/assets/.env",
            "https://appassets.androidplatform.net/assets/missing.svg",
        )) {
            val response = loader.intercept(Uri.parse(url))
            assertEquals(403, response.statusCode)
            assertEquals(0, requireNotNull(response.data).use { it.readBytes() }.size)
        }
    }
}
