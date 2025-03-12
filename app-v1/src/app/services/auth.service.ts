import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/';
  private tokenSubject = new BehaviorSubject<string | null>(localStorage.getItem('token'));
  token$ = this.tokenSubject.asObservable();

  constructor(private http: HttpClient) { }

  signup(username: string, email: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}signup/`, { username, email, password }).pipe(
      tap((response: any) => {
        this.setToken(response.token);
      })
    );
  }

  login(username: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}login/`, { username, password }).pipe(
      tap((response: any) => {
        this.setToken(response.token);
      })
    );
  }

  setToken(token: string) {
    localStorage.setItem('token', token);
    this.tokenSubject.next(token);
  }

  logout() {
    localStorage.removeItem('token');
    this.tokenSubject.next(null);
  }

  isAuthenticated(): boolean {
    return !!this.tokenSubject.value;
  }

  getToken(): string | null {
    return this.tokenSubject.value;
  }
}