<main class="container">
  <!-- Header with selectors and search bar -->
  <div class="header">
    <div class="options">
      <input list="versions" id="vers" name="vers" value="1.20.1" />
      <datalist id="versions">
        {#each versions as ver}
          {#if ver.type === "release"}
            <option value="{ver.id}"></option>
          {/if}
        {/each}
      </datalist>
      <input list="loaders" id="loaders-inp" name="loaders" value="forge"/>
      <datalist id="loaders">
        <option value="fabric"></option>
        <option value="forge"></option>
        <option value="neoforge"></option>
      </datalist>
    </div>
    <div class="search-container">
      <input type="text" placeholder="Search mods" spellcheck="false" id="searchinp" oninput={search} autocomplete="off" />
    </div>
  </div>

  <!-- Main content area -->
  <div class="content">
    <!-- Sidebar with selected mods -->
    <div class="sidebar">
      <div class="selected-mods">
        {#each selectedMods as mod}
          <div class="selected-mod">
            <span>{mod.name}</span>
            <button class="remove-btn" onclick={() => removeSelectedMod(mod.id)}>✕</button>
          </div>
        {/each}
      </div>
      <button class="action-button" onclick={install}>Install ({selectedMods.length})</button>
      <p>{status}</p>
    </div>

    <!-- Mods list -->
    <div class="mods">
      {#each mods as mod}
        {#if mod.project_type === "mod"}
          <Mod 
            icon_url={mod.icon_url} 
            title={mod.title} 
            description={mod.description} 
            project_id={mod.project_id}
            onclick={addMod} 
          />
        {/if}
      {/each}
    </div>
  </div>
</main>

<script lang="ts">
  import Mod from "../components/Mod.svelte";
  import { invoke } from '@tauri-apps/api/core';
  import { open } from '@tauri-apps/plugin-dialog';
  import { listen } from '@tauri-apps/api/event';

  let status = $state(" ")

  type Progress = {
    status: string
  }
  listen<Progress>("progress", (event) => {
    status = event.payload.status
  })

  let mods: {
    title: string;
    description: string;
    loaders: string[];
    versions: string[];
    icon_url: string;
    project_type: string;
    project_id: string;
  }[] = $state([]);

  // Create an array to store selected mods
  let selectedMods: {
    id: string;
    name: string;
  }[] = $state([]);

  async function install() {
    const version = document.getElementById("vers") as HTMLInputElement;
    const loader = document.getElementById("loaders-inp") as HTMLInputElement;
    const modIds = selectedMods.map(mod => mod.id);

    try {
      const selected = await open({
        directory: true,
        multiple: false,
        title: 'Select a folder'
      });

      if (selected) {
        console.log('Selected folder:', selected);
        invoke("install_mods", { mods: modIds, dir: selected, loader: loader.value, version: version.value })
      } else {
        console.log('No folder selected');
      }
    } catch (error) {
      console.error('Error selecting folder:', error);
    }
  }

  function removeSelectedMod(id: string) {
    selectedMods = selectedMods.filter(mod => mod.id !== id);
  }

  // Function to add a mod to selectedMods
  function addMod(id: string, name: string) {
    // Check if mod is already in the list to avoid duplicates
    if (!selectedMods.some(mod => mod.id === id)) {
      selectedMods = [...selectedMods, { id, name }];
      console.log("Added mod:", { id, name });
      console.log("Selected mods:", selectedMods);
    }
  }

  async function search(event: Event) {
    const target = event.target as HTMLInputElement;
    const version = document.getElementById("vers") as HTMLInputElement;
    const loader = document.getElementById("loaders-inp") as HTMLInputElement;

    fetch(`https://api.modrinth.com/v2/search?query=${target.value}&facets=[["versions:${version.value}"], ["categories:${loader.value}"]]`)
      .then((resp) => resp.json())
      .then((data) => {
        mods = data.hits;
        console.log(mods);
      });
  }

  let versions: { id: string; type: string }[] = $state([]);
  fetch("https://launchermeta.mojang.com/mc/game/version_manifest.json")
    .then((resp) => resp.json())
    .then((data) => {
      versions = data.versions;
    });
</script>

<style>
  :root {
    font-family: Inter, Avenir, Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 24px;
    font-weight: 400;
    color: #f6f6f6;
    background-color: #16181c;
    font-synthesis: none;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    -webkit-text-size-adjust: 100%;
  }

  /* Overall container remains full viewport */
  .container {
    margin: 0;
  }

  /* Header styling */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 80px;
    padding: 0 20px;
    background-color: #16181c;
    position: fixed;
    z-index: 2;
  }
  .options {
    display: flex;
    gap: 10px;
  }
  .search-container {
    flex: 1;
    display: flex;
    justify-content: flex-end;
    margin-left: 1.5rem;
  }

  /* Content area below header */
  .content {
    display: flex;
  }

  /* Sidebar fixed to left below header */
  .sidebar {
    position: fixed;
    top: 80px; /* height of header */
    left: 0;
    bottom: 0;
    width: 250px;
    display: flex;
    flex-direction: column;
    background-color: #1e2126;
    padding: 10px;
    box-sizing: border-box;
  }
  /* Scrollable area for selected mods within sidebar */
  .sidebar .selected-mods {
    flex: 1;
    overflow-y: auto;
    margin-bottom: 10px;
  }
  /* Fixed (sticky) button at bottom of sidebar */
  .sidebar .action-button {
    background-color: #33363d;
    color: #f6f6f6;
    border: none;
    border-radius: 10px;
    padding: 10px;
    cursor: pointer;
    position: sticky;
    bottom: 0;
  }

  /* Mods list area on the right */
  .mods {
    margin-left: 250px; /* equal to sidebar width */
    margin-top: 80px; /* equal to header height */
    padding: 20px;
    height: calc(100vh - 80px);
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
    box-sizing: border-box;
  }

  /* Inputs styling */
  #searchinp {
    background-color: #33363d;
    height: 40px;
    width: 450px;
    border: none;
    border-radius: 20px;
    color: #f6f6f6;
    text-align: center;
    font-size: 20px;
    outline: none;
  }
  #vers,
  #loaders-inp {
    background-color: #33363d;
    border: none;
    width: 85px;
    height: 40px;
    border-radius: 10px;
    color: #f6f6f6;
    text-align: center;
    font-size: 20px;
    outline: none;
  }
  .selected-mod {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #26292f;
    padding: 8px 12px;
    margin-bottom: 8px;
    border-radius: 8px;
  }

  .remove-btn {
    background: none;
    border: none;
    color: #b3b3b3;
    cursor: pointer;
    font-size: 14px;
    padding: 0 4px;
  }

  .remove-btn:hover {
    color: #f6f6f6;
  }
</style>
