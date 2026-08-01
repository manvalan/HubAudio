# HubAudio
# Power Management Architecture

**Document:** Power Management Design Specification  
**Revision:** 0.1  
**Status:** Design Phase  

---

# 1. Overview

The HubAudio platform requires a sophisticated power management architecture.

The system combines:

- ESP32-S3 high performance MCU with WiFi
- ADAU1467 professional audio DSP
- Si4684 FM/DAB receiver
- Bluetooth audio transmitter
- Bluetooth audio receiver
- battery operation
- remote monitoring capability


The power system is therefore not considered a simple voltage regulator stage, but a complete energy management subsystem.

---

# 2. Design Philosophy

The selected architecture follows these principles:

- single intelligent PMIC
- integrated battery management
- multiple independent power rails
- I2C monitoring
- controlled power sequencing
- ability to disable unused subsystems
- separated digital and audio power domains


---

# 3. Selected Main PMIC

## Texas Instruments TPS65217CRSLR


The TPS65217 is selected as the main power management IC.


Reasons for selection:


- integrated Li-Ion battery charger
- power path management
- multiple switching regulators
- LDO outputs
- I2C configuration
- programmable sequencing
- fault monitoring


Although originally designed for embedded processor systems, its architecture is suitable for HubAudio due to the need for multiple controlled power domains.


---

# 4. Power Tree


Proposed architecture:


             USB-C / External Power

                     |

                     |

             TPS65217CRSLR

                     |

    +----------------+----------------+

    |                |                |

 DCDC1             DCDC2            DCDC3

    |                |                |

3.3V_DIGITAL 3.3V_AUDIO 5V

    |                |

    |                |

ESP32-S3 Audio/RF domain

                |

          Ferrite filtering


                |

    +-----------+-----------+

    |           |           |

ADAU1467    Si4684      Bluetooth


---

# 5. Power Domains


## 5.1 Digital Domain


Voltage:

3.3V_DIGITAL


Consumers:


- ESP32-S3
- EEPROM
- logic peripherals
- communication interfaces


Requirements:


- high transient capability
- low impedance supply


Main concern:

ESP32-S3 WiFi current peaks.


---

# 5.2 Audio / RF Domain


Voltage:

3.3V_AUDIO


Consumers:


- ADAU1467
- Si4684
- BT1035
- Bluetooth RX module


This rail must be isolated from digital noise.


Recommended:



3.3V_AUDIO

  |

ferrite bead

  |

audio devices



---

# 5.3 5V Domain


Possible consumers:


- DAC
- amplifier
- future peripherals


This rail is kept independent from sensitive audio electronics.


---

# 6. Battery Management


The TPS65217 provides:


- Li-Ion charging
- battery monitoring
- power path control
- protection mechanisms


Battery:



Single cell Li-Ion

3.7V nominal

4.2V charged



---

# 7. Power Monitoring


## 7.1 Decision


The TPS65217 already provides battery management.

An additional current monitor is not required for system operation.


However, HubAudio benefits from detailed subsystem monitoring.


A dedicated I2C power monitor is therefore added for the audio domain.


---

# 8. Selected Current Monitor


## Texas Instruments INA226


The INA226 is selected as the default power monitoring device.


Purpose:


Measure the audio subsystem consumption.


Monitored rail:



TPS65217

|

3.3V_AUDIO

|

INA226

|

ADAU1467
Si4684
Bluetooth



---

# 9. INA226 Functions


The INA226 provides:


- bus voltage measurement
- shunt voltage measurement
- current measurement
- power calculation
- I2C communication


The ESP32-S3 can periodically read:



Voltage

Current

Power



Example:


```json
{
 "audio_voltage":3.30,
 "audio_current":180,
 "audio_power":0.59
}

10. INA228 Evaluation

The INA228 has been evaluated as an alternative.

Advantages:

higher resolution ADC
higher precision
energy accumulation
advanced power analysis

Typical application:

laboratory measurements
industrial systems
precision battery analysis

For HubAudio:

Not selected as default.

Reason:

The additional precision is not necessary because:

battery management is already handled by TPS65217
audio subsystem consumption does not require laboratory accuracy
11. Future Compatibility

The PCB should allow optional replacement:

INA226 footprint compatible with INA228 evaluation.

Possible versions:

Standard
TPS65217
+
INA226

Engineering / Pro Version
TPS65217
+
INA228

12. I2C Monitoring Bus

The power monitoring devices share the system I2C bus.

Example:

ESP32-S3


 |

I2C


 +---- EEPROM

 |

 +---- ADAU1467

 |

 +---- INA226

 |

 +---- TPS65217


13. Power Sequencing

Startup sequence:

Battery connected


 |

TPS65217 initialization


 |

3.3V_DIGITAL enabled


 |

ESP32-S3 boot


 |

Module detection


 |

Enable audio domain


 |

Initialize DSP


 |

Enable RF modules


14. Controlled Shutdown

The ESP32-S3 can disable:

Bluetooth TX
Bluetooth RX
Si4684
ADAU1467

Example:

Standby:


ESP32-S3 ON

WiFi ON

Audio OFF

Radio OFF

Bluetooth OFF


15. PCB Layout Requirements

Critical:

Switching regulators

Keep away from:

ADAU1467
DAC
RF sections
Audio supply

Use:

short traces
filtering
dedicated return paths
Decoupling

Every IC requires local decoupling.

Additional filtering is required for:

DSP supply
RF supply
16. Final Decision

The HubAudio power architecture is:

TPS65217CRSLR

+

Separate audio power domain

+

INA226 monitoring

+

Optional INA228 upgrade



This provides:

professional power management
battery operation
remote diagnostics
future scalability
END DOCUMENT

---