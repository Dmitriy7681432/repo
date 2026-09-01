/**
 * @file init/mh_init.h
 * @brief Переменная часть наработки
 * @author Катков А.Н.
 * @date 27.08.2020 г.
 * @version v.0.0.1a
 * @note БУ ЭА СВЭП-30М
 */

#ifndef SRC_INIT_MH_INIT_H_
#define SRC_INIT_MH_INIT_H_

#include "midlvl/models/param.h"
#include "generated/param_names.h"

#include "lowlvl/drivers/flash.h"

// Признаки
typedef union mh_attributes
{
	struct
	{
	// Требуется ТО ЭА
	uint8_t need_service_ea;
	// Требуется ТО ГТА
	uint8_t need_service_gta;
	// Резервы
	uint8_t reserv1;
	uint8_t reserv2;
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
	// Наработка ГТА
	uint32_t gta_mh;
	// Наработка ГТА с перегрузом в пределах 10 %
	uint32_t gta_mh10;
	// Признаки
	mh_attributes_t attribs;
	// Время ТО ЭА
	uint32_t ea_service_time;	
	// Время ТО ГТА
	uint32_t gta_service_time;	
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
	// Наработка ГТА
	uint32_t gta_mh;
	// Наработка ГТА с перегрузом в пределах 10 %
	uint32_t gta_mh10;
	// Признаки
	mh_attributes_t attribs;
	// Время ТО ЭА
	uint32_t ea_service_time;	
	// Время до ТО ЭА
	uint32_t ea_mh_left;	
	// Время ТО ГТА
	uint32_t gta_service_time;	
	// Время до ТО ГТА
	uint32_t gta_mh_left;	
	// Актуальный адрес
	uint32_t address;
}mh_data_t;

extern mutex_t motohours_mutex;

extern mh_data_t motohours_data;

extern mh_flash_t flash_record;

void read_record(uint32_t addr);

void write_record(uint32_t addr);

void set_zero_mh(void);

void flash_to_mh(void);

void mh_to_flash(void);

void params_to_mh(void);

void mh_to_params(void);

#endif /* SRC_INIT_MH_INIT_H_ */
