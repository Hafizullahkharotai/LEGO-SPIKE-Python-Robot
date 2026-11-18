import motor_pair
import color_sensor
import distance_sensor
from hub import port
import runloop
 
 
 
motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
 
# Svart linje → reflekterer lite lys → lav verdi (ca. 10–30)
# Hvitt gulv → reflekterer mye lys → høy verdi (ca. 60–90)
#
# Derfor bruker vi en grenseverdi:
# svart < GRENSEVERDI
# hvitt > GRENSEVERDI
GRENSEVERDI = 35
 
async def main():
    Steering = "none"
 
    while True:
 
 
        left = color_sensor.reflection(port.D)
        right = color_sensor.reflection(port.C)
       
        # Both white: drive straight along the track
        if left > GRENSEVERDI and right > GRENSEVERDI:
            motor_pair.move_tank(motor_pair.PAIR_1, -500, -500)
 
        # Both black = INTERSECTION: drive straight and ignore the sensors for a while
        elif left < GRENSEVERDI and right < GRENSEVERDI:
            if(Steering == "Left"):
                motor_pair.move_tank(motor_pair.PAIR_1, -300, -450)
            elif(Steering == "Right"):
                motor_pair.move_tank(motor_pair.PAIR_1, -450, -300)
            motor_pair.move_tank(motor_pair.PAIR_1, -200, -200)
            await runloop.sleep_ms(100)
 
        # Only left sensor sees black: correct the direction
        elif left < GRENSEVERDI:
            Steering = "Left"
            motor_pair.move_tank(motor_pair.PAIR_1, -500, -50)
 
        # Only right sensor sees black: correct the direction
        elif right < GRENSEVERDI:
            Steering = "Right"
            motor_pair.move_tank(motor_pair.PAIR_1, -50, -200)
 
        # Short pause so the hub can keep up
        await runloop.sleep_ms(10)
 
 
runloop.run(main())
