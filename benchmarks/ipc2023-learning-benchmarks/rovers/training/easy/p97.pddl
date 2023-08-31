;; rovers=4, waypoints=10, cameras=4, objectives=10, out_folder=training/easy, instance_id=97, seed=132

(define (problem rover-97)
 (:domain rover)
 (:objects 
    general - lander
    colour high_res low_res - mode
    rover1 rover2 rover3 rover4 - rover
    rover1store rover2store rover3store rover4store - store
    waypoint1 waypoint2 waypoint3 waypoint4 waypoint5 waypoint6 waypoint7 waypoint8 waypoint9 waypoint10 - waypoint
    camera1 camera2 camera3 camera4 - camera
    objective1 objective2 objective3 objective4 objective5 objective6 objective7 objective8 objective9 objective10 - objective)
 (:init 
    (at_lander general waypoint7)
    (at rover1 waypoint3)
    (at rover2 waypoint7)
    (at rover3 waypoint1)
    (at rover4 waypoint3)
    (equipped_for_soil_analysis rover3)
    (equipped_for_rock_analysis rover3)
    (equipped_for_rock_analysis rover2)
    (equipped_for_imaging rover1)
    (equipped_for_imaging rover2)
    (empty rover1store)
    (empty rover2store)
    (empty rover3store)
    (empty rover4store)
    (store_of rover1store rover1)
    (store_of rover2store rover2)
    (store_of rover3store rover3)
    (store_of rover4store rover4)
    (at_rock_sample waypoint5)
    (at_rock_sample waypoint6)
    (at_rock_sample waypoint7)
    (at_rock_sample waypoint9)
    (at_rock_sample waypoint10)
    (at_soil_sample waypoint2)
    (at_soil_sample waypoint6)
    (at_soil_sample waypoint7)
    (at_soil_sample waypoint9)
    (at_soil_sample waypoint10)
    (visible waypoint6 waypoint2)
    (visible waypoint1 waypoint2)
    (visible waypoint7 waypoint1)
    (visible waypoint2 waypoint1)
    (visible waypoint8 waypoint4)
    (visible waypoint3 waypoint1)
    (visible waypoint4 waypoint6)
    (visible waypoint9 waypoint2)
    (visible waypoint5 waypoint7)
    (visible waypoint6 waypoint4)
    (visible waypoint2 waypoint9)
    (visible waypoint1 waypoint7)
    (visible waypoint10 waypoint6)
    (visible waypoint6 waypoint10)
    (visible waypoint2 waypoint6)
    (visible waypoint4 waypoint8)
    (visible waypoint7 waypoint5)
    (visible waypoint1 waypoint3)
    (visible waypoint6 waypoint7)
    (visible waypoint7 waypoint6)
    (visible waypoint4 waypoint9)
    (visible waypoint9 waypoint4)
    (visible waypoint9 waypoint10)
    (visible waypoint10 waypoint9)
    (visible waypoint3 waypoint10)
    (visible waypoint10 waypoint3)
    (visible waypoint1 waypoint9)
    (visible waypoint9 waypoint1)
    (visible waypoint2 waypoint3)
    (visible waypoint3 waypoint2)
    (visible waypoint7 waypoint9)
    (visible waypoint9 waypoint7)
    (visible waypoint3 waypoint8)
    (visible waypoint8 waypoint3)
    (can_traverse rover1 waypoint6 waypoint2)
    (can_traverse rover1 waypoint1 waypoint2)
    (can_traverse rover1 waypoint7 waypoint1)
    (can_traverse rover1 waypoint2 waypoint1)
    (can_traverse rover1 waypoint8 waypoint4)
    (can_traverse rover1 waypoint3 waypoint1)
    (can_traverse rover1 waypoint4 waypoint6)
    (can_traverse rover1 waypoint9 waypoint2)
    (can_traverse rover1 waypoint5 waypoint7)
    (can_traverse rover1 waypoint6 waypoint4)
    (can_traverse rover1 waypoint2 waypoint9)
    (can_traverse rover1 waypoint1 waypoint7)
    (can_traverse rover1 waypoint10 waypoint6)
    (can_traverse rover1 waypoint6 waypoint10)
    (can_traverse rover1 waypoint2 waypoint6)
    (can_traverse rover1 waypoint4 waypoint8)
    (can_traverse rover1 waypoint7 waypoint5)
    (can_traverse rover1 waypoint1 waypoint3)
    (can_traverse rover1 waypoint1 waypoint9)
    (can_traverse rover1 waypoint9 waypoint1)
    (can_traverse rover1 waypoint7 waypoint9)
    (can_traverse rover1 waypoint9 waypoint7)
    (can_traverse rover1 waypoint3 waypoint8)
    (can_traverse rover1 waypoint8 waypoint3)
    (can_traverse rover2 waypoint6 waypoint2)
    (can_traverse rover2 waypoint1 waypoint2)
    (can_traverse rover2 waypoint7 waypoint1)
    (can_traverse rover2 waypoint2 waypoint1)
    (can_traverse rover2 waypoint8 waypoint4)
    (can_traverse rover2 waypoint3 waypoint1)
    (can_traverse rover2 waypoint4 waypoint6)
    (can_traverse rover2 waypoint9 waypoint2)
    (can_traverse rover2 waypoint5 waypoint7)
    (can_traverse rover2 waypoint6 waypoint4)
    (can_traverse rover2 waypoint2 waypoint9)
    (can_traverse rover2 waypoint1 waypoint7)
    (can_traverse rover2 waypoint10 waypoint6)
    (can_traverse rover2 waypoint6 waypoint10)
    (can_traverse rover2 waypoint2 waypoint6)
    (can_traverse rover2 waypoint4 waypoint8)
    (can_traverse rover2 waypoint7 waypoint5)
    (can_traverse rover2 waypoint1 waypoint3)
    (can_traverse rover2 waypoint6 waypoint7)
    (can_traverse rover2 waypoint7 waypoint6)
    (can_traverse rover2 waypoint2 waypoint3)
    (can_traverse rover2 waypoint3 waypoint2)
    (can_traverse rover3 waypoint6 waypoint2)
    (can_traverse rover3 waypoint1 waypoint2)
    (can_traverse rover3 waypoint7 waypoint1)
    (can_traverse rover3 waypoint2 waypoint1)
    (can_traverse rover3 waypoint8 waypoint4)
    (can_traverse rover3 waypoint3 waypoint1)
    (can_traverse rover3 waypoint4 waypoint6)
    (can_traverse rover3 waypoint9 waypoint2)
    (can_traverse rover3 waypoint5 waypoint7)
    (can_traverse rover3 waypoint6 waypoint4)
    (can_traverse rover3 waypoint2 waypoint9)
    (can_traverse rover3 waypoint1 waypoint7)
    (can_traverse rover3 waypoint10 waypoint6)
    (can_traverse rover3 waypoint6 waypoint10)
    (can_traverse rover3 waypoint2 waypoint6)
    (can_traverse rover3 waypoint4 waypoint8)
    (can_traverse rover3 waypoint7 waypoint5)
    (can_traverse rover3 waypoint1 waypoint3)
    (can_traverse rover3 waypoint4 waypoint9)
    (can_traverse rover3 waypoint9 waypoint4)
    (can_traverse rover3 waypoint3 waypoint10)
    (can_traverse rover3 waypoint10 waypoint3)
    (can_traverse rover3 waypoint1 waypoint9)
    (can_traverse rover3 waypoint9 waypoint1)
    (can_traverse rover3 waypoint3 waypoint8)
    (can_traverse rover3 waypoint8 waypoint3)
    (can_traverse rover4 waypoint6 waypoint2)
    (can_traverse rover4 waypoint1 waypoint2)
    (can_traverse rover4 waypoint7 waypoint1)
    (can_traverse rover4 waypoint2 waypoint1)
    (can_traverse rover4 waypoint8 waypoint4)
    (can_traverse rover4 waypoint3 waypoint1)
    (can_traverse rover4 waypoint4 waypoint6)
    (can_traverse rover4 waypoint9 waypoint2)
    (can_traverse rover4 waypoint5 waypoint7)
    (can_traverse rover4 waypoint6 waypoint4)
    (can_traverse rover4 waypoint2 waypoint9)
    (can_traverse rover4 waypoint1 waypoint7)
    (can_traverse rover4 waypoint10 waypoint6)
    (can_traverse rover4 waypoint6 waypoint10)
    (can_traverse rover4 waypoint2 waypoint6)
    (can_traverse rover4 waypoint4 waypoint8)
    (can_traverse rover4 waypoint7 waypoint5)
    (can_traverse rover4 waypoint1 waypoint3)
    (calibration_target camera1 objective2)
    (on_board camera1 rover2)
    (supports camera1 colour)
    (supports camera1 high_res)
    (supports camera1 low_res)
    (calibration_target camera2 objective5)
    (on_board camera2 rover2)
    (supports camera2 high_res)
    (supports camera2 low_res)
    (calibration_target camera3 objective4)
    (on_board camera3 rover1)
    (supports camera3 high_res)
    (supports camera3 colour)
    (calibration_target camera4 objective9)
    (on_board camera4 rover2)
    (supports camera4 colour)
    (visible_from objective1 waypoint9)
    (visible_from objective1 waypoint4)
    (visible_from objective1 waypoint6)
    (visible_from objective1 waypoint7)
    (visible_from objective1 waypoint5)
    (visible_from objective1 waypoint1)
    (visible_from objective1 waypoint3)
    (visible_from objective1 waypoint10)
    (visible_from objective2 waypoint1)
    (visible_from objective2 waypoint6)
    (visible_from objective2 waypoint7)
    (visible_from objective2 waypoint5)
    (visible_from objective2 waypoint3)
    (visible_from objective2 waypoint2)
    (visible_from objective2 waypoint10)
    (visible_from objective2 waypoint9)
    (visible_from objective3 waypoint4)
    (visible_from objective3 waypoint2)
    (visible_from objective3 waypoint6)
    (visible_from objective3 waypoint10)
    (visible_from objective3 waypoint7)
    (visible_from objective4 waypoint6)
    (visible_from objective4 waypoint7)
    (visible_from objective4 waypoint10)
    (visible_from objective4 waypoint4)
    (visible_from objective4 waypoint2)
    (visible_from objective4 waypoint5)
    (visible_from objective4 waypoint9)
    (visible_from objective4 waypoint8)
    (visible_from objective5 waypoint7)
    (visible_from objective5 waypoint10)
    (visible_from objective5 waypoint3)
    (visible_from objective5 waypoint1)
    (visible_from objective5 waypoint9)
    (visible_from objective6 waypoint9)
    (visible_from objective6 waypoint10)
    (visible_from objective6 waypoint2)
    (visible_from objective6 waypoint7)
    (visible_from objective6 waypoint3)
    (visible_from objective6 waypoint1)
    (visible_from objective6 waypoint5)
    (visible_from objective6 waypoint4)
    (visible_from objective6 waypoint8)
    (visible_from objective7 waypoint4)
    (visible_from objective7 waypoint1)
    (visible_from objective7 waypoint5)
    (visible_from objective7 waypoint3)
    (visible_from objective7 waypoint9)
    (visible_from objective8 waypoint9)
    (visible_from objective8 waypoint3)
    (visible_from objective8 waypoint7)
    (visible_from objective8 waypoint2)
    (visible_from objective8 waypoint8)
    (visible_from objective9 waypoint10)
    (visible_from objective9 waypoint5)
    (visible_from objective9 waypoint7)
    (visible_from objective9 waypoint8)
    (visible_from objective9 waypoint6)
    (visible_from objective9 waypoint3)
    (visible_from objective9 waypoint9)
    (visible_from objective9 waypoint2)
    (visible_from objective10 waypoint5)
    (visible_from objective10 waypoint1)
    (visible_from objective10 waypoint7)
    (visible_from objective10 waypoint2)
    (visible_from objective10 waypoint4)
    (visible_from objective10 waypoint8)
    (visible_from objective10 waypoint10)
    (visible_from objective10 waypoint6)
    (visible_from objective10 waypoint3))
 (:goal  (and 
    
    (communicated_soil_data waypoint7)
    (communicated_soil_data waypoint6)
    (communicated_image_data objective2 high_res))))
