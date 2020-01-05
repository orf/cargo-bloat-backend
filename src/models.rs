#[derive(Queryable)]
pub struct Installation {
    pub id: i32,
    pub installation_id: i32,
    pub repo: String,
}
