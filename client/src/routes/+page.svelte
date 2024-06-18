<script lang="ts">
    import SlideList from "../components/SlideList.svelte";
    import SlideViewer from "../components/SlideViewer.svelte";
    import {currentSlideID} from "../stores.js";
    import UploadForm from "../components/UploadForm.svelte";
    import {onMount} from "svelte";

    let slideId: string | null
    currentSlideID.subscribe(value => slideId = value)
    let slideList: Array<string> = []

    let getSlideList = async () => {
        let response = await fetch("http://localhost:8000/api/ ")
        console.log("запрос")
        slideList = await response.json()
    }

    const slideIdReset = () => slideId = null
    onMount(async () => {
        await getSlideList()
    })
    $: slideList = [...slideList]

</script>

<div id="main">
    <div id="slide">
        {#key slideId}
            <SlideViewer id={slideId}/>
        {/key}
    </div>
    <div id="right">
        <div id="slide-list">
            <SlideList slideList={slideList}
                       on:update={async () => {await getSlideList();
                       slideIdReset()}}/>
        </div>
        <div id="upload-form">
            <UploadForm on:update={async () => await getSlideList()}/>
        </div>
    </div>
</div>
<div id="manual">
    <h2>ЫнструкцЫя</h2>
    <ol>
        <li>качаешь тестовые данные по
            <a href="https://openslide.cs.cmu.edu/download/openslide-testdata/">этой</a>
            ссылке
        </li>
        <li>пихаешь скачанный файл в форму. (название обязательное, описание не очень)</li>
        <li>жмешь "загрузить слайд"</li>
        <li>ждешь пока в списке не появится загруженный файл</li>
        <li>щелкаешь на него и приближаешь удаляешь и т д и т п</li>
    </ol>
    <h2>Примечания</h2>
    <ul>
        <li>интерфейс - дерьмо, но я и не фронтовик. все делалось ради бэкенда</li>
        <li>все ошибки которые могут случаться можно увидеть только в консоли. нигде и никуда я ничего не выводил</li>
        <li>ошибки отлажены не все. например точно знаю что не все форматы из тестовых данных будут работать. вопрос какие конкретно</li>
        <li></li>
    </ul>
</div>

<style>
    #main {
        display: flex;
        height: 90vh;
        border: 2px black solid;
        padding: 0;
        margin: 0;
    }

    #slide {
        border: 2px black solid;
        margin: 5px;
        width: 100%;
    }

    #right {
        width: 40%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 15px;
    }

    #upload-form {
        width: 100%;
    }

    #slide-list {
        overflow-y: scroll;
        margin-bottom: 10px;
    }
    #manual{
        margin-left: 50px;
    }
</style>
