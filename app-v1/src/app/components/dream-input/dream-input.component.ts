// import { Component, OnInit } from '@angular/core';
// import { DreamService } from '../../services/dream.service';
// import { HttpClientModule } from '@angular/common/http';
// import { FormsModule } from '@angular/forms'
// import { MatInputModule } from '@angular/material/input';
// import { MatButtonModule } from '@angular/material/button'
// import { AuthService } from '../../services/auth.service';
// import { Router } from '@angular/router';
// import { CommonModule } from '@angular/common';

// @Component({
//   selector: 'app-dream-input',
//   imports: [HttpClientModule,
//     CommonModule,
//     FormsModule,
//     MatInputModule,
//     MatButtonModule,],
//   templateUrl: './dream-input.component.html',
//   styleUrls: ['./dream-input.component.scss']
// })
// export class DreamInputComponent implements OnInit {
//   prompt = '';
//   dreamOutput = '';

  

//   constructor(
//     private dreamService: DreamService,
//     private authService: AuthService,
//     private router: Router
//   ) { }

//   ngOnInit() {
//     if (!this.authService.isAuthenticated()) {
//       this.router.navigate(['/login']);
//     }
//   }

//   generateDream() {
//     this.dreamService.streamDream(this.prompt).subscribe({
//       next:dream => {
//       this.dreamOutput = dream;
//       },
//       error: error => {
//         console.error('Error generating dream:', error);
//         }
//     });
//   }

//   logout() {
//     this.authService.logout();
//     this.router.navigate(['/login']);
//   }
// }


import { Component, OnInit } from '@angular/core';
import { DreamService } from '../../services/dream.service';
import { AuthService } from '../../services/auth.service';
import { Router, RouterModule } from '@angular/router';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';

@Component({
  selector: 'app-dream-input',
  imports: [HttpClientModule,
    CommonModule,
    FormsModule,
    MatInputModule,
    RouterModule,
    MatButtonModule,
    MatSelectModule
  ],
  templateUrl: './dream-input.component.html',
  styleUrls: ['./dream-input.component.scss']
})
export class DreamInputComponent implements OnInit {
  prompt = '';
  style = 'default';
  dreamOutput = '';
  error = '';

  constructor(
    private dreamService: DreamService,
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit() {
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/login']);
    }
  }

  generateDream() {
    this.error = '';
    this.dreamService.generateDream(this.prompt, this.style).subscribe({
      next: (response: any) => {
        this.dreamOutput = response.dream;
      },
      error: (err) => {
        this.error = err.error?.error || 'Failed to generate dream.';
        console.error('HTTP error:', err);
      }
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}