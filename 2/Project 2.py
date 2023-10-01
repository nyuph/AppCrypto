from enigma.rotors.rotor import Rotor
from enigma.plugboard import Plugboard
from enigma.machine import EnigmaMachine

rL = Rotor('my rotor1', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', ring_setting=0, stepping='Q')
rM = Rotor('my rotor2', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', ring_setting=5, stepping='V')
rR = Rotor('my rotor3', 'ESOVPZJAYQUIRHXLNFTGKDCMWB', ring_setting=10, stepping='J')

reflector = Rotor('my reflector', 'YRUHQSLDPXNGOKMIEBFZCWVJAT')

# With plugboard
pb = Plugboard.from_key_sheet('AK BZ CG DL FU HJ MX NR OY PW')
print("pb", pb)

# Without plugboard
#pb = Plugboard.from_key_sheet('')

machine = EnigmaMachine([rL, rM, rR], reflector, pb)

machine.set_display('UPS')       # set rotor positions or use its default
position = machine.get_display()    # read rotor position
print("position:",position)

# Encrypt A letter
#print(machine.key_press('C'))
# Encrypt a text
print(machine.process_text('MachineaenigmaaisapowerfulaforaQ'))

# Decrypt a text
#print(machine.process_text('XWLLLTABMLCYXINVCJAWMASCSBKKTSVO'))