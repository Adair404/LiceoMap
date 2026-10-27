package com.liceomap.app.ui.map

import org.junit.Assert.assertEquals
import org.junit.Test

class MapBoundsTest {
    @Test fun fullMapCannotBeDraggedOffScreen() {
        assertEquals(MapViewport(), MapViewport().fitTransform(300f, 300f, 100f, 100f, 999f, -999f))
    }
    @Test fun zoomedMapStopsAtItsEdges() {
        assertEquals(MapViewport(2f, 150f, -150f),
            MapViewport().fitTransform(300f, 300f, 100f, 100f, 999f, -999f, 2f))
    }
    @Test fun gestureKeepsItsFocusAndZoomOutReturnsToFullMap() {
        val enlarged = MapViewport().fitTransform(300f, 300f, 100f, 100f, zoom = 2f, focusX = 50f)
        assertEquals(MapViewport(2f, -50f, 0f), enlarged)
        assertEquals(MapViewport(), enlarged.fitTransform(300f, 300f, 100f, 100f, zoom = 0.1f))
    }
}
