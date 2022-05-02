import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';

import { JwtService } from './jwt.service';
import { catchError } from 'rxjs/operators';

@Injectable()
export class ApiService {
    constructor(
        private http: HttpClient,
        private jwtService: JwtService
    ) { }

    private formatErrors(error: any) {
        return throwError(error.error);
    }

    get(path: string, params: HttpParams = new HttpParams()): Observable<any> {
        return this.http.get(`api/${path}/`, { params })
            .pipe(catchError(this.formatErrors));
    }

    put(path: string, body: Object = {}): Observable<any> {
        return this.http.put(
            `api/${path}/`,
            JSON.stringify(body)
        ).pipe(catchError(this.formatErrors));
    }

    post(path: string, body: Object = {}): Observable<any> {
        return this.http.post(
            `api/${path}/`,
            JSON.stringify(body)
        ).pipe(catchError(this.formatErrors));
    }

    delete(path: string): Observable<any> {
        return this.http.delete(
            `api/${path}/`
        ).pipe(catchError(this.formatErrors));
    }
}
