import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DreamInputComponent } from './dream-input.component';

describe('DreamInputComponent', () => {
  let component: DreamInputComponent;
  let fixture: ComponentFixture<DreamInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DreamInputComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DreamInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
