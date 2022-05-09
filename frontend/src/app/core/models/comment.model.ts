import { Thumbnail } from './thumbnail.model';

export class Comment {
    id: string;
    content: string;
    replies: Comment[];
    author: Thumbnail;
    canModify: boolean;
    createdAt: string;

    constructor(
        id: string,
        content: string,
        replies: Comment[],
        author: Thumbnail,
        canModify: boolean,
        createdAt: string
    ) {
        this.id = id;
        this.content = content;
        this.replies = replies;
        this.author = author;
        this.canModify = canModify;
        this.createdAt = createdAt;
    }
}