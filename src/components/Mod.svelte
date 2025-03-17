<main class="mod-container">
  <img src={icon_url} alt="Icon" />
  <div class="info">
    <div class="title-container">
      <h3>{title}</h3>
      <button class="small-btn" on:click={() => onclick(project_id, title)}>Add</button>
    </div>
    <p>{description}</p>
  </div>
</main>

<script>
  export let icon_url;
  export let title;
  export let description;
  export let onclick;
  export let project_id;
</script>

<style>
  .mod-container {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 10px;
    border-radius: 15px;
    background-color: #26292f;
  }
  .mod-container img {
    width: 60px;
    height: 60px;
    flex-shrink: 0;
    border-radius: 10px;
  }
  .info {
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: left;
  }
  .title-container {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .info h3 {
    margin: 0;
    font-size: 18px;
  }
  .info p {
    margin: 0;
    font-size: 12px;
    color: #b3b3b3;
  }
  .small-btn {
    padding: 5px 12px;
    font-size: 12px;
    border: none;
    border-radius: 5px;
    background-color: #4a4f58;
    color: white;
    cursor: pointer;
  }
  .small-btn:hover {
    background-color: #5a5f68;
  }
</style>
