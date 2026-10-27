package com.liceomap.app.ui.map

/** Presentation state and gesture calculation, independent of Compose and Android. */
data class MapViewport(val scale: Float = 1f, val x: Float = 0f, val y: Float = 0f) {
    fun transform(panX: Float, panY: Float, zoom: Float) = copy(
        scale = (scale * zoom).coerceIn(0.8f, 3f),
        x = x + panX,
        y = y + panY,
    )
}

/** Keep the fitted image visible, including after zooming out or rotating the screen. */
fun MapViewport.fitTransform(
    viewWidth: Float, viewHeight: Float, imageWidth: Float, imageHeight: Float,
    panX: Float = 0f, panY: Float = 0f, zoom: Float = 1f,
    focusX: Float = 0f, focusY: Float = 0f,
): MapViewport {
    if (viewWidth <= 0f || viewHeight <= 0f || imageWidth <= 0f || imageHeight <= 0f) return this
    val nextScale = (scale * zoom).coerceIn(1f, 6f)
    val ratio = nextScale / scale
    val fit = minOf(viewWidth / imageWidth, viewHeight / imageHeight)
    val boundX = ((imageWidth * fit * nextScale - viewWidth) / 2f).coerceAtLeast(0f)
    val boundY = ((imageHeight * fit * nextScale - viewHeight) / 2f).coerceAtLeast(0f)
    return MapViewport(nextScale,
        if (boundX == 0f) 0f else (x * ratio + focusX * (1f - ratio) + panX).coerceIn(-boundX, boundX),
        if (boundY == 0f) 0f else (y * ratio + focusY * (1f - ratio) + panY).coerceIn(-boundY, boundY))
}
