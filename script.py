import powerstand as ips
import powerstand

psm = powerstand.init()
print("Ход:\t", psm.tick)

consumption = 0
for i in psm.houses:
    consumption += i.forecast[0]
for i in psm.hospitals:
    consumption += i.forecast[0]
for i in psm.factories:
    consumption += i.forecast[0]

generation = 0
for i in psm.wind_gens:
    generation += i.value
for i in psm.sun_gens:
    generation += i.value

generation *= 0.75
consumption *= 1.25
shortage = consumption - generation
charge = psm.grav.charge
print("Избытки:\t", shortage)
print("Сохранено:\t", charge)

if shortage > 0:
    if shortage < charge:
        psm.orders.grav.discharge(abs(shortage))
        print("Взято:\t", charge)
    else:
        psm.orders.grav.discharge(charge)
        psm.orders.external.buy(shortage - charge, 1)
        print("Взято:\t",charge)
        print("Куплено:\t",shortage - charge)
else:
    if charge < psm.grav.capacity:
        if charge + abs(shortage) < psm.grav.capacity:
            give = abs(shortage)
            print("Отдано:\t",give)
            if give > psm.grav.charge_rate:
                rate = psm.grav.charge_rate
                psm.orders.grav.charge(rate)
                psm.orders.external.sell(give - rate, 1)
            else:
                psm.orders.grav.charge(give / 4)
                psm.orders.external.sell(give*0.75, 1)
        else:
            print("Отдано:\t", abs(shortage))
            psm.orders.grav.charge(psm.grav.capacity - charge)
            psm.orders.external.sell(abs(shortage) - (psm.grav.capacity - charge), 1)
            print("Продано:\t", abs(shortage) - (psm.grav.capacity - charge))
    else:
        print("Продано:\t", abs(shortage))
        psm.orders.external.sell(abs(shortage), 1)
psm.save_and_exit()