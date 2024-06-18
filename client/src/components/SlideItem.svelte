<script>
    import {createEventDispatcher} from "svelte";
    import {currentSlideID} from "../stores.js";

    export let id
    export let title
    export let description = null

    // trigger event and send object
    function setCurrentSlideID() {
        currentSlideID.update(() => id)
    }
    const dispatch = createEventDispatcher();

    function updateSlideList() {
        dispatch('update');
    }
    async function deleteSlide(event) {
        const result = await fetch(`http://localhost:8000/api/${id}`,
            {method: "DELETE"})
        if (result.ok) {
            updateSlideList()
        }
    }

</script>

<div class="item" on:click={setCurrentSlideID}>
<!--    <img src="{id}" alt="no preview">-->
    <div class="slide-info">
        <h4>{title}</h4>
        <p>{description}</p>
    </div>
    <button on:click|stopPropagation={deleteSlide}>x</button>
</div>


<style>
    .item {
        display: flex;
        background: aqua;
        padding: 10px;
        margin: 15px;
        justify-content: space-between;

    }

    img {
        width: 80px;
        height: 60px;
        border: 1px black solid;
    }

    .slide-info {
        margin-left: 5px;
    }

    h4 {
        padding: 0;
        margin: 0;
    }

    p {
        margin: 0;
        padding: 0;
        font-size: 14px;
    }
</style>