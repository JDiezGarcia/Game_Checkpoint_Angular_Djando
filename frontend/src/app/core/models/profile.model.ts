export class Profile {
    email: string;
    username: string;
    name: string;
    image: string;
    title: string;
    following: boolean;
    comments: Comment[];

    constructor(
        email: string,
        username: string,
        name: string,
        image: string,
        title: string,
        following: boolean,
        comments: Comment[]
    ) {
        this.email = email;
        this.username = username;
        this.name = name;
        this.image = image;
        this.title = title;
        this.following = following;
        this.comments = comments;
    }
}