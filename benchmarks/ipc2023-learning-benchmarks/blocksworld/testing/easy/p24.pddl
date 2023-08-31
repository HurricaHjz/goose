;; blocks=24, out_folder=testing/easy, instance_id=24, seed=1030

(define (problem blocksworld-24)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 b14 b15 b16 b17 b18 b19 b20 b21 b22 b23 b24 - object)
 (:init 
    (arm-empty)
    (clear b22)
    (on b22 b24)
    (on-table b24)
    (clear b5)
    (on b5 b12)
    (on b12 b21)
    (on b21 b19)
    (on-table b19)
    (clear b23)
    (on b23 b9)
    (on b9 b18)
    (on b18 b10)
    (on b10 b1)
    (on b1 b4)
    (on b4 b16)
    (on b16 b11)
    (on b11 b8)
    (on b8 b3)
    (on b3 b13)
    (on-table b13)
    (clear b17)
    (on b17 b15)
    (on b15 b7)
    (on b7 b6)
    (on b6 b20)
    (on b20 b14)
    (on b14 b2)
    (on-table b2))
 (:goal  (and 
    (clear b13)
    (on-table b13)
    (clear b17)
    (on b17 b15)
    (on b15 b21)
    (on b21 b18)
    (on b18 b12)
    (on b12 b4)
    (on b4 b19)
    (on b19 b7)
    (on b7 b3)
    (on b3 b8)
    (on b8 b24)
    (on b24 b10)
    (on b10 b5)
    (on b5 b22)
    (on b22 b23)
    (on b23 b9)
    (on b9 b14)
    (on b14 b1)
    (on b1 b11)
    (on b11 b2)
    (on b2 b6)
    (on b6 b16)
    (on b16 b20)
    (on-table b20))))
