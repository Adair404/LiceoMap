package com.liceomap.app.ui.map

import android.graphics.BitmapFactory
import android.util.Log
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.FitScreen
import androidx.compose.material.icons.filled.Remove
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.listSaver
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.unit.IntSize
import androidx.compose.ui.unit.dp
import com.liceomap.app.model.DemoRooms
import com.liceomap.app.model.LoadState
import com.liceomap.app.model.RoomId
import com.liceomap.app.ui.components.StatusCard
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

private val MapViewportSaver = listSaver<MapViewport, Float>(
    save = { listOf(it.scale, it.x, it.y) },
    restore = { MapViewport(it[0], it[1], it[2]) },
)

/** Native, offline raster of the unchanged canonical SVG; no browser is involved. */
@Composable
fun MapScreen(selectedRoom: RoomId? = null) {
    val context = LocalContext.current.applicationContext
    var reload by remember { mutableStateOf(0) }
    val map by produceState<LoadState<ImageBitmap>>(LoadState.Loading, context, reload) {
        value = LoadState.Loading
        value = try {
            val bitmap = withContext(Dispatchers.IO) {
                context.assets.open("mapa_liceo_concepto.png").use {
                    requireNotNull(BitmapFactory.decodeStream(it)) { "Invalid packaged PNG" }.asImageBitmap()
                }
            }
            Log.i("LiceoMapViewer", "Native PNG decoded: ${bitmap.width}x${bitmap.height}")
            LoadState.Ready(bitmap)
        } catch (error: Exception) {
            Log.e("LiceoMapViewer", "Cannot decode packaged school map", error)
            LoadState.Error("No pudimos abrir el mapa del liceo.")
        }
    }
    var viewport by rememberSaveable(stateSaver = MapViewportSaver) { mutableStateOf(MapViewport()) }
    var mapSize by remember { mutableStateOf(IntSize.Zero) }
    val image = (map as? LoadState.Ready)?.data
    fun zoom(factor: Float) {
        image?.let {
            viewport = viewport.fitTransform(mapSize.width.toFloat(), mapSize.height.toFloat(),
                it.width.toFloat(), it.height.toFloat(), zoom = factor)
        }
    }
    LaunchedEffect(mapSize, image) {
        image?.let {
            Log.i("LiceoMapViewer", "Native map viewport: ${mapSize.width}x${mapSize.height}")
            viewport = viewport.fitTransform(mapSize.width.toFloat(), mapSize.height.toFloat(),
                it.width.toFloat(), it.height.toFloat())
        }
    }

    Column(Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
        Box(Modifier.weight(1f).fillMaxWidth().clipToBounds().onSizeChanged { mapSize = it }) {
            when (val state = map) {
                LoadState.Loading -> CircularProgressIndicator(Modifier.align(Alignment.Center).testTag("map-loading"))
                is LoadState.Error -> Box(Modifier.align(Alignment.Center).padding(20.dp)) {
                    StatusCard("Mapa no disponible", state.message, onRetry = { reload += 1 })
                }
                is LoadState.Ready -> Image(
                    bitmap = state.data,
                    contentDescription = "Mapa real del liceo",
                    contentScale = ContentScale.Fit,
                    modifier = Modifier.fillMaxSize().testTag("school-map")
                        .semantics { stateDescription = "Zoom ${(viewport.scale * 100).toInt()}%" }
                        .pointerInput(state.data, mapSize) {
                            detectTransformGestures { centroid, pan, factor, _ ->
                                viewport = viewport.fitTransform(size.width.toFloat(), size.height.toFloat(),
                                    state.data.width.toFloat(), state.data.height.toFloat(), pan.x, pan.y, factor,
                                    centroid.x - size.width / 2f, centroid.y - size.height / 2f)
                            }
                        }
                        .graphicsLayer(scaleX = viewport.scale, scaleY = viewport.scale,
                            translationX = viewport.x, translationY = viewport.y),
                )
            }
            if (image != null) Column(Modifier.align(Alignment.TopEnd).padding(8.dp)) {
                FilledTonalIconButton(onClick = { zoom(1.5f) }, modifier = Modifier.testTag("map-zoom-in")) {
                    Icon(Icons.Default.Add, contentDescription = "Ampliar mapa")
                }
                FilledTonalIconButton(onClick = { zoom(1f / 1.5f) }, modifier = Modifier.testTag("map-zoom-out")) {
                    Icon(Icons.Default.Remove, contentDescription = "Reducir mapa")
                }
                FilledTonalIconButton(onClick = { viewport = MapViewport() }, modifier = Modifier.testTag("map-reset")) {
                    Icon(Icons.Default.FitScreen, contentDescription = "Ver mapa completo")
                }
            }
        }
        Column(Modifier.fillMaxWidth().background(MaterialTheme.colorScheme.surface).padding(16.dp)) {
            Text(selectedRoom?.let { DemoRooms.find(it)?.label ?: "Sala seleccionada" } ?: "Mapa del liceo",
                style = MaterialTheme.typography.titleSmall)
            if (selectedRoom != null) Text("La ubicación de esta sala aún no está vinculada al mapa.",
                style = MaterialTheme.typography.bodySmall)
            Text("Pellizca para ampliar y arrastra para desplazarte", style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}
