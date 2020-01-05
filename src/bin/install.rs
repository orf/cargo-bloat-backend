use cargo_bloat_backend::establish_connection;
use cargo_bloat_backend::models::*;

use diesel::prelude::*;

use lambda_http::{lambda, IntoResponse, Request};
use lambda_runtime::{error::HandlerError, Context};
use serde_json::json;

fn main() {
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
        .expect("Error loading posts");

    println!("Displaying {} posts", results.len());
    for r in results {
        println!("{} / {} / {}", r.id, r.installation_id, r.repo);
    }
    Ok(json!({
        "message": "Go Serverless v1.0! Your function executed successfully!"
    }))
}
