#[macro_use]
extern crate diesel;
#[macro_use]
extern crate diesel_migrations;

pub mod models;
pub mod schema;

use diesel::pg::PgConnection;
use diesel_migrations::embed_migrations;
use diesel::prelude::*;
use dotenv::dotenv;
use std::env;

embed_migrations!("migrations/");

pub fn establish_connection() -> PgConnection {
    dotenv().ok();

    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    let conn = PgConnection::establish(&database_url)
        .unwrap_or_else(|_| panic!("Error connecting to {}", database_url));
    embedded_migrations::run_with_output(&conn, &mut std::io::stdout());
    return conn;
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
