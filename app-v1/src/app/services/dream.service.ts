import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class DreamService {
  private apiUrl = 'http://localhost:8000/api/';

  constructor(private http: HttpClient, private authService: AuthService) { }

  generateDream(prompt: string, style: string): Observable<any> {
    const headers = new HttpHeaders().set('Authorization', `Token ${this.authService.getToken()}`);
    return this.http.post(`${this.apiUrl}generate/`, { prompt, style }, { headers });
  }

  getDreamHistory(page: number = 1): Observable<any> {
    const headers = new HttpHeaders().set('Authorization', `Token ${this.authService.getToken()}`);
    return this.http.get(`${this.apiUrl}dreams/?page=${page}`, { headers });
  }

  deleteDream(dreamId: number): Observable<any> {
    const headers = new HttpHeaders().set('Authorization', `Token ${this.authService.getToken()}`);
    return this.http.delete(`${this.apiUrl}dreams/${dreamId}/`, { headers });
  }
}