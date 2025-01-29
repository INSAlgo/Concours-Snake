use std::io::stdin;

type Result<T, E = Box<dyn std::error::Error>> = std::result::Result<T, E>;

fn main() -> Result<()> {

    let mut buffer = String::new();

    stdin().read_line(&mut buffer)?;

    stdin().read_line(&mut buffer)?;
    let vec: Vec<&str> = buffer.trim_end().split(' ').collect();

    stdin().read_line(&mut buffer)?;
    stdin().read_line(&mut buffer)?;

    if vec[1]=="2" {
        stdin().read_line(&mut buffer)?;
    }

    loop {
        println!("right");
        stdin().read_line(&mut buffer)?;
    }
}