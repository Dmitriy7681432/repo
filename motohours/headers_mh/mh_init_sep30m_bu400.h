/**
 * @file init/mh_init.h
 * @brief Переменная часть наработки
 * @author Катков А.Н.
 * @date 28.04.2021 г.
 * @version v.0.0.1a
 * @note БУ 400 СЭП-30М
 */

#ifndef SRC_INIT_MH_INIT_H_
#define SRC_INIT_MH_INIT_H_

#include "midlvl/models/param.h"
#include "lowlvl/drivers/flash.h"

// Адрес последней записи в секторе 7.
// Запись занимает 12 байт, в секторе умещается 21845 записей.
//#define MOTOHOURS_LAST_ADDR ((uint32_t)0xBFDFFFF0)

// Запись во флеш
typedef struct mh_flash
{
	// Наработка СПЧ
	uint32_t spch_mh;
	// Наработка СПЧ2
	uint32_t spch2_mh;
	// Наработка СИПТ
	uint32_t sipt_mh;
}mh_flash_t;

// Структура данных в ОЗУ
typedef struct mh_data
{
	// Наработка СПЧ
	uint32_t spch_mh;
	// Наработка СПЧ2
	uint32_t spch2_mh;
	// Наработка СИПТ
	uint32_t sipt_mh;
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
