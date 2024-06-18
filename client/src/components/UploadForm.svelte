<script>
    import {createEventDispatcher} from "svelte";

    let file;
    let title = '';
    let description = '';
    let filename = "Выберите файл"

    const dispatch = createEventDispatcher();

    function updateSlideList() {
        dispatch('update');
    }

    $: if(file) filename = file.name

    async function uploadFile() {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('title', title);
        formData.append('description', description);

        const response = await fetch('http://localhost:8000/', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            console.log('файл успешно загружен');
            updateSlideList()
        } else {
            console.error('Ошибка при загрузке данных');
        }
    }
</script>

<div>
    <input
            type="text"
           bind:value="{title}"
           placeholder="название">
    <textarea
            bind:value="{description}"
            placeholder="Описание"
            rows="7"
    ></textarea>
    <label class="input-file">
        <input type="file"
               accept="
               .svs,
               .tif,
               .dcm,
               .vms,
               .vmu,
               .ndpi,
               .scn,
               .mrxs,
               .tiff,
               .svsslide,
               .bif,
               .czi
"
               on:change="{(event) => file = event.target.files[0]}">
        <span>{filename}</span>
        <progress
                id="progress"
                aria-label="Фид обновляется"
                value=0
                max=100
        ></progress>
    </label>
    <button on:click="{uploadFile}">загрузить слайд</button>
</div>


<style>
    div{
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: space-around;
        width: 100%;
    }

    div > *{
        width: 100%;
        margin: 0;
        padding: 0;
    }
    div > *:not(:last-child) {
        margin-bottom: 3px; /* Отступ снизу для всех элементов, кроме последнего */
    }

    textarea{
        resize: none;
    }
    .input-file {
        position: relative;
        display: inline-block;
        width: 100%;
    }
    .input-file span {
        position: relative;
        display: inline-block;
        width: 100%;
        cursor: pointer;
        outline: none;
        text-decoration: none;
        font-size: 14px;
        vertical-align: middle;
        color: rgb(255 255 255);
        text-align: center;
        border-radius: 4px;
        background-color: #419152;
        line-height: 11px;
        height: 30px;
        padding: 10px 20px;
        box-sizing: border-box;
        border: none;
        margin: 0;
        transition: background-color 0.2s;
    }
    .input-file input[type=file] {
        position: absolute;
        z-index: -1;
        opacity: 0;
        display: block;
        width: 0;
        height: 0;
    }

    /* Focus */
    .input-file input[type=file]:focus + span {
        box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
    }

    /* Hover/active */
    .input-file:hover span {
        background-color: #59be6e;
    }
    .input-file:active span {
        background-color: #2E703A;
    }

    /* Disabled */
    .input-file input[type=file]:disabled + span {
        background-color: #eee;
    }

</style>