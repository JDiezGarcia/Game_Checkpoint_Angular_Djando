export class User {
    email: string;
    username: string;
    name: string;
    img: string;
    title: string;
    token: string;
    role: string;

    constructor(
        email: string,
        username: string,
        name: string,
        img: string,
        title: string,
        token: string,
        role: string
    ) {
        this.email = email;
        this.username = username;
        this.name = name;
        this.img = img;
        this.title = title;
        this.token = token;
        this.role = role;
    }
}
