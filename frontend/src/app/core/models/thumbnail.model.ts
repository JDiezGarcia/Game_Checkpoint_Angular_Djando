export class Thumbnail {
    username: string;
    image: string;
    title: string;
    constructor(
        username: string,
        image: string,
        title: string,
    ) {
        this.username = username;
        this.image = image;
        this.title = title;
    }
}