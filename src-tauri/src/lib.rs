// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
use tauri::{AppHandle, Emitter};
use serde::Serialize;

#[derive(Clone, Serialize)]
struct Progress<'a> {
  status: &'a str
}

#[tauri::command]
async fn install_mods(
    app: AppHandle,
    mods: Vec<String>,
    dir: String,
    loader: String,
    version: String,
) -> Result<(), String> {
    println!("installing to {}", dir);

    let modrinth = ferinth::Ferinth::default();
    let client = reqwest::Client::new();

    for mod_id in mods {
        let versions = modrinth
            .list_versions_filtered(&mod_id, Some(&[&loader]), Some(&[&version]), None)
            .await
            .map_err(|e| e.to_string())?;
        println!("{}", versions[0].name);

        println!(
            "downloading {} as {}",
            versions[0].files[0].url,
            versions[0].files[0].filename
        );
        app.emit("progress", Progress { status: &versions[0].files[0].filename }).unwrap();

        let response = client
            .get(versions[0].files[0].url.clone())
            .send()
            .await
            .map_err(|e| e.to_string())?;
        let bytes = response
            .bytes()
            .await
            .map_err(|e| e.to_string())?;

        let path = format!("{}\\{}", dir, versions[0].files[0].filename);
        tokio::fs::write(path, bytes)
            .await
            .map_err(|e| e.to_string())?;
    }

    app.emit("progress", Progress { status: "Done" }).unwrap();
    Ok(())
}


#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![install_mods])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
