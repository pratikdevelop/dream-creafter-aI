import { Component, OnInit } from '@angular/core';
import { DreamService } from '../../services/dream.service';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card'
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-dream-history',
  imports: [
    CommonModule,
    MatCardModule
  ],
  templateUrl: './dream-history.component.html',
  styleUrls: ['./dream-history.component.scss']
})
export class DreamHistoryComponent implements OnInit {
  dreams: any[] = [];
  error = '';

  constructor(
    private dreamService: DreamService,
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit() {
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/login']);
    } else {
      this.loadDreams();
    }
  }

  loadDreams() {
    this.dreamService.getDreamHistory().subscribe({
      next: (data) => {
        console.log(
          'ss', data
        );
        
        this.dreams = data.dreams;
      },
      error: (err) => {
        this.error = 'Failed to load dream history.';
        console.error('History error:', err);
      }
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}