use cargo_bloat_backend::establish_connection;
use cargo_bloat_backend::models::*;

use diesel::prelude::*;

use lambda_http::{lambda, IntoResponse, Request, RequestExt};
use lambda_runtime::{error::HandlerError, Context};
use serde_json::json;
use serde_derive::{Serialize, Deserialize};

#[derive(Deserialize)]
struct Repository {
    full_name: String,
}

#[derive(Deserialize)]
enum InstallationEventAction {
    Created,
    Deleted,
}

#[derive(Deserialize)]
struct InstallationEvent {
    action: InstallationEventAction,
    repositories: Option<Vec<Repository>>,
}

#[derive(Deserialize)]
enum InstallationRepositoriesEventAction {
    Added,
    Removed,
}

#[derive(Deserialize)]
struct InstallationRepositoriesEvent {
    action: InstallationEventAction,
    repositories_added: Vec<Repository>,
    repositories_removed: Vec<Repository>,
}

fn main() {
    establish_connection();
    lambda!(handler)
}


fn handler(_: Request, _: Context) -> Result<impl IntoResponse, HandlerError> {
    // `serde_json::Values` impl `IntoResponse` by default
    // creating an application/json response
    use cargo_bloat_backend::schema::installs::dsl::*;

    let connection = establish_connection();

    let results = installs
        .filter(installation_id.eq(1))
        .load::<Installation>(&connection)
        .expect("Error loading results");

    Ok(json!({
        "message": "Go Serverless v1.0! Your function executed successfully!"
    }))
}
