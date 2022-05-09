export class Thumbnail {
    username: string;
    img: string;
    title: string;
    constructor(
        username: string,
        img: string,
        title: string,
    ) {
        this.username = username;
        this.img = img;
        this.title = title;
    }
}