<script>
    import {onDestroy, onMount} from 'svelte';

    export let id
    let viewer

    onMount(async () => {
        if(id)
        {
            const result = await fetch(`http://localhost:8000/api/${id}/dimensions`)
            const {width, height} = await result.json()
            const OpenSeadragon = await import('openseadragon');
            viewer = OpenSeadragon.default({
                id: "osd-viewer",
                prefixUrl: "node_modules/openseadragon/build/openseadragon/images/",
                tileSources: {
                    tileSize: 256,
                    minLevel: 8,
                    height: height,
                    width: width,
                    getTileUrl: function (level, x, y) {
                        return `http://localhost:8000/${id}/${level}/${x}/${y}`
                    }
                }
            });
            viewer.addHandler('tile-loaded', function (event) {
                let tile = event.tile;
                let tiledImage = event.tiledImage;

                let loadingTiles = tiledImage.lastDrawn.filter(function (t) {
                    return t.loading;
                });

                if (loadingTiles.length > 0) {
                    tile.loading = false;
                    viewer.forceRedraw();
                }
            });
        }

    });
    onDestroy(() => {
        if (viewer) viewer.destroy()
    })
</script>

<div id="osd-viewer" style="width: 100%; height: 100%;"></div>

<style>

</style>