;Evan Gray - May 2012
;Run: racket Helper.rkt
#lang racket
(require "rktAI.rkt")
(define frames 0)
(define (loop) 
  (set! frames (+ 1 frames))
  (if (equal? frames 20)
      ((lambda ()
        (thrust 1)
        (set! frames 0)))
      (thrust 0))
  (turnLeft 1)
  (fireShot))
(start loop '("-name" "Relper"))