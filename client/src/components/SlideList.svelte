<script>
    import SlideItem from "./SlideItem.svelte";

    export let slideList = []


</script>


{#each slideList as slide (slide["ID"])}
    <SlideItem id={slide['ID']}
               title={slide.title}
               description={slide.description}
               on:update
    />
{/each}
