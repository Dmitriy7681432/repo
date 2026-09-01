/**
 * @file init/mh_init.h
 * @brief Переменная часть наработки
 * @author Катков А.Н.
 * @date 28.08.2020 г.
 * @version v.0.0.1a
 * @note БУ СВЭП СВЭП-30М
 */

#ifndef SRC_INIT_MH_INIT_H_
#define SRC_INIT_MH_INIT_H_

#include "midlvl/models/param.h"
#include "lowlvl/drivers/flash.h"

//!!! Пересчитать. Взято из БУ СЭП СЭП-30М для тестовой сборки проекта.
// Адрес последней записи в секторе 7.
// Запись занимает 20 байт, в секторе умещается 13107 записей.
#define MOTOHOURS_LAST_ADDR ((uint32_t)0xBFDBFFC0)

// Признаки
typedef union mh_attributes
{
	struct
	{
	// Требуется ТО ЭА
	uint8_t need_service_ea;
	// Резервы
	uint8_t reserv1;
	uint8_t reserv2;
	uint8_t reserv3;
	};
	uint32_t word;
}mh_attributes_t;

// Запись во флеш
typedef struct mh_flash
{
	// Наработка станции
	uint32_t station_mh;
	// Наработка ЭА
	uint32_t ea_mh;
	// Наработка ЭА с перегрузом в пределах 10 %
	uint32_t ea_mh10;
	// Наработка ПЧ1
	uint32_t fc1_mh;
	// Наработка ПЧ2
	uint32_t fc2_mh;
	// Наработка СИПТ
	uint32_t sipt_mh;
	// Признаки
	mh_attributes_t attribs;
	// Время ТО ЭА
	uint32_t ea_service_time;
}mh_flash_t;

// Структура данных в ОЗУ
typedef struct mh_data
{
	// Наработка станции
	uint32_t station_mh;
	// Наработка ЭА
	uint32_t ea_mh;
	// Наработка ЭА с перегрузом в пределах 10 %
	uint32_t ea_mh10;
	// Наработка ПЧ1
	uint32_t fc1_mh;
	// Наработка ПЧ2
	uint32_t fc2_mh;
	// Наработка СИПТ
	uint32_t sipt_mh;
	// Признаки
	mh_attributes_t attribs;
	// Время ТО ЭА
	uint32_t ea_service_time;
	// Время до ТО ЭА
	uint32_t ea_mh_left;
	// Актуальный адрес
	uint32_t address;
}mh_data_t;

extern mutex_t motohours_mutex;

extern mh_data_t motohours_data;

extern mh_flash_t flash_record;

// Чтение записи из флеш в переменную flash_record с указанного адреса
void read_record(uint32_t addr);

// Запись переменной flash_record во флеш по указанному адресу
void write_record(uint32_t addr);

// Обнуление структуры данных в ОЗУ
void set_zero_mh(void);

// Копирование структуры данных в переменную flash_record
void flash_to_mh(void);

// Копирование из переменной flash_record в структуру данных в ОЗУ
void mh_to_flash(void);

// Копирование значений параметров наработки в структуру данных в ОЗУ
void params_to_mh(void);

// Копирование значений из структуры данных в ОЗУ в параметры наработки
void mh_to_params(void);
#endif /* SRC_INIT_MH_INIT_H_ */
