package com.liceomap.app.ui.map

import android.content.Context
import android.net.Uri
import android.webkit.WebResourceResponse
import androidx.webkit.WebViewAssetLoader
import java.io.ByteArrayInputStream

internal const val MAP_PAGE_URL = "https://appassets.androidplatform.net/assets/mapa.html"
internal const val MAP_SVG_URL = "https://appassets.androidplatform.net/assets/mapa_liceo_concepto.svg"

/** Serve only the two packaged map resources. Never fall back to the network. */
internal class SchoolMapAssets(context: Context) {
    private val loader = WebViewAssetLoader.Builder()
        .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(context.applicationContext))
        .build()

    fun intercept(url: Uri): WebResourceResponse {
        val mimeType = when (url.toString()) {
            MAP_PAGE_URL -> "text/html"
            MAP_SVG_URL -> "image/svg+xml"
            else -> return errorResponse(403, "Forbidden")
        }
        val response = loader.shouldInterceptRequest(url) ?: return errorResponse(404, "Not Found")
        if (response.data == null) return errorResponse(404, "Not Found")
        response.mimeType = mimeType
        response.encoding = "UTF-8"
        response.responseHeaders = mapOf(
            "Cache-Control" to "no-store",
            "X-Content-Type-Options" to "nosniff",
        )
        return response
    }

    private fun errorResponse(status: Int, reason: String) = WebResourceResponse(
        "text/plain", "UTF-8", status, reason,
        mapOf("Cache-Control" to "no-store"), ByteArrayInputStream(ByteArray(0)),
    )
}
