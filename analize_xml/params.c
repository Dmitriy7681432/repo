﻿#line 2 "params.c"
/**
 * @file init/params.c
 * @brief Инициализация массива структур описаний параметров
 * @author Катков А.Н.
 * @date 15.01.2020 г.
 * @version v.0.0.1a
 * @note БУ СВЭП СВЭП-30М
 * @author Катков А.Н.
 * @date 14.05.2020 г.
 * @version v.0.0.2a
 * @note Добавил функцию, вызываемую задачей приема данных по CAN
 * @author Никонов С.Ю.
 * @date 28.03.2022 г.
 * @version v.0.0.3
 * @note Добавил шапки в бинарные файлы 
 */


#include <runtime/lib.h>
#include <kernel/uos.h>
#include <runtime/math.h>

#include "init/limits.h"
#include "highlvl/helpers/memory.h"

#include "highlvl/net1.h"
#include "highlvl/analize_alarm.h"

#include "lowlvl/modules/module.h"
#include "lowlvl/modules/mod380.h"
#include "lowlvl/modules/mod420.h"
#include "lowlvl/modules/discr.h"
#include "lowlvl/modules/relay.h"
#include "lowlvl/modules/intercom/intercom.h"
#include "lowlvl/drivers/controller_bus.h"

#include "midlvl/models/bin_file_header.h"
#include "midlvl/models/param.h"
#include "midlvl/models/cont.h"
#include "midlvl/models/periodic.h"
#include "midlvl/models/preset.h"
#include "midlvl/models/cosinus.h"
#include "midlvl/sqrt.h"
#include "midlvl/motohours.h"

#include "init/params.h"
#include "generated/system_description.h"
#include "generated/data_keys.h"

#include "generated/param_names.h"
#include "generated/calibration_names.h"
#include "midlvl/filter.h"
#include "midlvl/calibr.h"
#include "highlvl/system_config.h"
#include "highlvl/fc_ad.h"
#include "highlvl/diesel-generator.h"
#include "highlvl/startstopmode.h"
#include "highlvl/power-source.h"

extern uint32_t prev_react;

// Данные параметров.
float coefs[CALIBRATION_NAMES_COUNTER];
TParam param[CNT_PRM];

// Объекты контакторов (объявление в файле init/conts.c)
extern TCont cont[CNT_CONT];

// Объекты событий (объявление в файле init/alarm.c)
extern TAlarm alarm[EVENT_NAMES_COUNTER];

static TPerItem paritems[CNT_PRM];
TPeriodic params_periodic;
static TPerItem paritems_A4[CNT_PRM];
TPeriodic params_periodic_A4;
static TPerItem paritems_A5[CNT_PRM];
TPeriodic params_periodic_A5;
static TPerItem paritems_A6[CNT_PRM];
TPeriodic params_periodic_A6;

// Шапка preset
bin_file_header_t preset_header;
// Шапка calibration
bin_file_header_t calibration_header;
// Шапка filter
bin_file_header_t filter_header;

uint32_t filters_addresses_lengths[FILTERS_SETT_LENGTH];

extern task_t*	start_task;
extern task_t*	stop_task;

extern uint32_t crc32b(const void *data, uint32_t len);


/** @note Адреса уставок, калибровок, конфигурации системы смотрите в документе TAKI00039-01 81 05. Krivenko 31.03.2022
*/
// Адрес массива уставок в ПЗУ - сектор 5 флеш-памяти, смещение 0
#define PRESET_ADDR ((uint32_t)0xBFD40000)
// Адрес массива калибровок в ПЗУ - сектор 5 флеш-памяти, смещение 8 кБ
#define CALIBR_ADDR ((uint32_t)0xBFD42000)
// Адрес массива адресов и длин фильтров в ПЗУ - сектор 5 флеш-памяти, смещение 16 кБ
#define FILTERS_SETT_ADDR ((uint32_t)0xBFD44000)

// Адрес наработок в ПЗУ - сектор 7 флеш-памяти
#define MOTOHOURS_ADDR ((uint32_t)0xBFDC0000)

// Адрес настроек в ПЗУ - сектор 4 флеш-памяти
#define SETTINGS_ADDR ((uint32_t)0xBFD00000)

// Версия ВПО модуля управления - 1.0.0
#define SOFTWARE_VERSION ((uint32_t)0x00010000)

extern timer_t timer;

// метка времени для вычисления градиента
//static uint32_t timestamp_gradient = 0;
//****************************************************************************************************
/**
 *  @brief Выводит сообщение об ошибке.
 *  @param num [in] Номер параметра, в котором произошла ошибка.
 */
__attribute__((unused)) static void params_error(int16_t num)
{
	debug_printf("ERR! param[%d] %s\r", num, param[num].name);
}
//****************************************************************************************************
/**
 *  @brief 
 *  @param item [in] 
 *  @return 
 */
static int8_t params_periodic_call(TPerItem* item)
{
	TParam* param = (TParam*)item->data;
	return param_renew(param);
}

//****************************************************************************************************
int8_t init_discrete(param_names_t name_param, TModulesEn module_number, uint32_t channel, char* name_string, uint16_t period)
{
	int8_t err = 0;

	param[name_param].name 		= name_string;
	param[name_param].type 		= PARAM_TYPE_REPORT;
	param[name_param].module 	= &module[module_number];
	param[name_param].addrr		= channel;
	param[name_param].read 		= mod_discr_get;

	err	 = param_init(&param[name_param]);

	err += periodic_add_item(&params_periodic, &param[name_param], param[name_param].name, period);
	return err;
}// end of init_discrete
//****************************************************************************************************
// Метка времени
int8_t get_time_stamp(void *prm)
{

	TParam *loc_prm = (TParam*)prm;

	loc_prm->value.val_int = timer_milliseconds(&timer);
	return 0;
}
//****************************************************************************************************
int8_t param_calibr_line_voltage (float *coef, uint32_t data_in, float *data_out)
{
	// y = kx + b

	// k - *coef
	// b - *(coef + 1)

	float local = 0;
	uint32_t theshold_data_in = 0; 
	theshold_data_in = preset[s_298_].cur_value.val_int;

	(data_in <= theshold_data_in) ? (local = 0) : (local = ((*coef) * data_in) + (*(coef + 1)));
	(local >= 0) ? (*data_out = local) : (*data_out = 0.0);

	return 0;
}
//****************************************************************************************************
int8_t param_calibr_line_frequency_net (float *coef, uint32_t data_in, float *data_out)
{
	// y = kx + b
	// k - *coef
	// b - *(coef + 1)

	float local = 0, tmp = 0, theshold_data_out = 0;
	read_data_element(N_U_AB, &tmp, 4);	
	theshold_data_out = preset[s_299_].cur_value.val_f;
	
	(data_in == 0) ? (local = 0) : (local = ((*coef) * data_in) + (*(coef + 1)));
	(local >= 0) ? (*data_out = local) : (*data_out = 0.0);	
	if(tmp <=theshold_data_out) (*data_out = 0.0);
	
	return 0;
}
//****************************************************************************************************
// Расчет времени наработки станции
int8_t calc_station_motohours(void* val)
{
	TParam *loc_prm = (TParam*)val;

    if(((param[NSTATE].value.val_int == 2) && param[NCONT].value.val_int == 1) || 
		((param[EASTATE].value.val_int == 4) || (param[EASTATE].value.val_int == 5)) ||
		((param[N2STATE].value.val_int == 2) && param[N2CONT].value.val_int == 1))
	// Добавляем к значению 30 секунд
	loc_prm->value.val_int += 30;

	return 0;
}
//****************************************************************************************************
int8_t param_calibr_line_frequency_net2 (float *coef, uint32_t data_in, float *data_out)
{
	// y = kx + b

	// k - *coef
	// b - *(coef + 1)

	float local = 0, tmp = 0, theshold_data_out = 0;
	read_data_element(N2_U_AB, &tmp, 4);	
	theshold_data_out = preset[s_299_].cur_value.val_f;
	
	(data_in == 0) ? (local = 0) : (local = ((*coef) * data_in) + (*(coef + 1)));
	(local >= 0) ? (*data_out = local) : (*data_out = 0.0);	
	if(tmp <=theshold_data_out) (*data_out = 0.0);
	
	return 0;
}
//****************************************************************************************************
int8_t param_calibr_line_frequency_ea (float *coef, uint32_t data_in, float *data_out)
{
	// y = kx + b

	// k - *coef
	// b - *(coef + 1)

	float local = 0, tmp = 0, theshold_data_out = 0;
	read_data_element(EA_U_AB, &tmp, 4);	
	theshold_data_out = preset[s_299_].cur_value.val_f;
	
	(data_in == 0) ? (local = 0) : (local = ((*coef) * data_in) + (*(coef + 1)));
	(local >= 0) ? (*data_out = local) : (*data_out = 0.0);	
	if(tmp <=theshold_data_out) (*data_out = 0.0);
	
	return 0;
}
//****************************************************************************************************
// Активная мощность Сети1
int8_t calc_p_net1(void* val)
{
	float ua = 0, ub = 0, ia = 0, ib = 0;
	int32_t phiua = 0,phiub = 0, phiia = 0, phiic = 0;
	int32_t delta_aui = 0, delta_bui = 0;

	TParam *loc_prm = (TParam*)val;
	
	ua = param[NUAB].value.val_f;
	ub = param[NUBC].value.val_f;
	ia = param[NIA].value.val_f;
	ib = param[NIB].value.val_f;
	phiua = param[NPHIUA].value.val_int;
	phiub = param[NPHIUB].value.val_int;
	phiia = param[NPHIIA].value.val_int;
	phiic = param[NPHIIC].value.val_int;
	/*
	 debug_printf("%s %d NIA %f\n\r",__FILE__,__LINE__,ia);
	 debug_printf("%s %d NIB %f\n\r",__FILE__,__LINE__,ib);
	 debug_printf("%s %d NPHIUA %d\n\r",__FILE__,__LINE__,param[NPHIUA].value.val_int);
	 debug_printf("%s %d NPHIUB %d\n\r",__FILE__,__LINE__,param[NPHIUB].value.val_int);
	 debug_printf("%s %d NPHIUC %d\n\r",__FILE__,__LINE__,param[NPHIUC].value.val_int);
	 debug_printf("%s %d NPHIIA %d\n\r",__FILE__,__LINE__,param[NPHIIA].value.val_int);
	 debug_printf("%s %d NPHIIB %d\n\r",__FILE__,__LINE__,param[NPHIIB].value.val_int);
	 debug_printf("%s %d NPHIIC %d\n\r",__FILE__,__LINE__,param[NPHIIC].value.val_int);
	 debug_printf("%s %d cosinus(phiua - phiia) %f\n\r",__FILE__,__LINE__,cosinus(phiua - phiia));
	 debug_printf("%s %d cosinus(phiub - phiib) %f\n\r",__FILE__,__LINE__,cosinus(phiub - phiib));
	*/
	
	(phiua>phiia)?(delta_aui=((360-phiua)+phiia)):(delta_aui = phiia-phiua);
	(phiub>phiic)?(delta_bui=((360-phiub)+phiic)):(delta_bui = phiic-phiub);
//	 debug_printf("%s %d cosinus(delta_aui) %f\n\r","kr",__LINE__,cosinus(delta_aui));
//	 debug_printf("%s %d cosinus(delta_bui) %f\n\r","kr",__LINE__,cosinus(delta_bui));
	
//	 debug_printf("%s %d delta_aui %d delta_bui %d \n\r",__FILE__,__LINE__,delta_aui, delta_bui);
	
	loc_prm->value.val_f = (ua * ia * cosinus(delta_aui) - 
		ub * ib * cosinus(delta_bui))/1000.0;
   
//my_debug
   //if(loc_prm->value.val_f<0)
   // {
   //     loc_prm->value.val_f = (ua * ia * cosinus(delta_aui) - 
   //       ub * ib * cosinus(delta_bui))/-1000.0;
   // }
    //debug_printf("%s %d loc_prm->value.val_f %f\n\r","kr",__LINE__,loc_prm->value.val_f);

  return 0;
}// end of calc_p_net1
//****************************************************************************************************
// Реактивная мощность Сети1
int8_t calc_q_net1(void* val)
{
	float ua = 0,ub = 0,ia = 0,ic = 0;
	int32_t phiua = 0,phiub = 0,phiia =0,phiic =0;
	int32_t delta_aui = 0, delta_bui = 0;

	TParam *loc_prm = (TParam*)val;

	ua = param[NUAB].value.val_f;
	ub = param[NUBC].value.val_f;
	ia = param[NIA].value.val_f;
	ic = param[NIC].value.val_f;
	phiua = param[NPHIUA].value.val_int;
	phiub = param[NPHIUB].value.val_int;
	phiia = param[NPHIIA].value.val_int;
	phiic = param[NPHIIC].value.val_int;
	
    (phiua>phiia)?(delta_aui=((360-phiua)+phiia)):(delta_aui = phiia-phiua);
	(phiub>phiic)?(delta_bui=((360-phiub)+phiic)):(delta_bui = phiic-phiub);

	loc_prm->value.val_f = (ua * ia * cosinus(90-(delta_aui)) -
		 ub * ic * cosinus(90-(delta_bui)))/1000.0;
//	loc_prm->value.val_f = (ua * ia * cosinus(90-(phiua - phiia)) -
//		 ub * ic * cosinus(90-(phiub - phiic)))/1000.0;

	return 0;
}//calc_q_net1
//****************************************************************************************************
// Полная мощность Сети1
int8_t calc_s_net1(void* val)
{
	float np, nq;

	TParam *loc_prm = (TParam*)val;

	np = param[NP].value.val_f;
	nq = param[NQ].value.val_f;

	loc_prm->value.val_f = sqrtf(np * np + nq * nq);

	return 0;
}
//****************************************************************************************************
// Косинус Сети1
int8_t calc_cos_net1(void* val)
{
	float np, ns; uint8_t ncont;

	TParam *loc_prm = (TParam*)val;
	
  read_data_element(N_CONT, &ncont, 4);	

	np = param[NP].value.val_f;
	ns = param[NS].value.val_f;
  if(ncont==1) loc_prm->value.val_f = (ns < 0.1) ? 1: np/ns;
  if(ncont==0) loc_prm->value.val_f = 0.0;
	
	return 0;
}
//****************************************************************************************************
/** @details Функция для определения неверной фазировки Сети.
	Неверная фазировка определяется наличием напряжением, находящимся в норме, и неверным углом между напряжениями.
	@return 0 - в любом случае. В параметр пишется 0 - фазировка в норме; 1 - неверная фазировка.
*/
int8_t calc_incorrect_net1(void* val)
{
	int32_t delta_phiab = 0, delta_phibc = 0;
	int32_t phiua = 0,phiub = 0, phiuc = 0;
	float nuab = 0, nubc = 0,  nuac = 0, set_282_uhigh = 0, set_283_umin = 0;
	
	TParam *loc_prm = (TParam*)val;
	
	nuab = param[NUAB].value.val_f;
	nubc = param[NUBC].value.val_f;
	nuac = param[NUAC].value.val_f;

	phiua = param[NPHIUA].value.val_int;
	phiub = param[NPHIUB].value.val_int;
	phiuc = param[NPHIUC].value.val_int;
	
	read_data_element(s_282, &set_282_uhigh, sizeof(set_282_uhigh));
	read_data_element(s_283, &set_283_umin, sizeof(set_283_umin));	
	// debug_printf("NPHIUA %d\n\r",param[NPHIUA].value.val_int);
	// debug_printf("NPHIUB %d\n\r",param[NPHIUB].value.val_int);	
	// debug_printf("NPHIUC %d\n\r",param[NPHIUC].value.val_int);
	
	if( (nuab>set_283_umin) && (nuab<set_282_uhigh) &&
		(nubc>set_283_umin) && (nubc<set_282_uhigh)	&&
		(nuac>set_283_umin) && (nuac<set_282_uhigh))
		{// если амлитуда напряжения в норме, то смотрим фазы	
	
			(phiua > phiub)?(delta_phiab = (360 - phiua)+phiub):(delta_phiab = phiub - phiua);
			(phiub > phiuc)?(delta_phibc = (360 - phiub)+phiuc):(delta_phibc = phiuc - phiub);
	
			// debug_printf("%s %d delta_phiab %d, delta_phibc %d \n\r",__FILE__, __LINE__, delta_phiab, delta_phibc);
	
			if(((delta_phiab < (120+10)) && (delta_phiab>(120-10))))
			{	
				loc_prm->value.val_int = 0;
			}
			else
			{
			loc_prm->value.val_int = 1;
			}
		}
	return 0;
}//calc_incorrect_net1
//****************************************************************************************************
/** @details calc_break_net1 Функция вычисления обрыва сети.
	@return 0 - нет обрыва, 1 - обрыв одной из фаз ВИП.
*/
int8_t calc_break_net1(void* val)
{
	float nuab = 0, nubc = 0, nuac = 0, const_u = 295.0;
	uint32_t res = 0;

	TParam *loc_prm = (TParam*)val;

	// uint32_t phiua = param[NPHIUA].value.val_int;
	// uint32_t phiub = param[NPHIUB].value.val_int;
	// uint32_t phiuc = param[NPHIUC].value.val_int;
	nuab = param[NUAB].value.val_f;
	nubc = param[NUBC].value.val_f;
	nuac = param[NUAC].value.val_f;
	
	// debug_printf("%s %d phiua	%d\n\r",__FILE__,__LINE__,phiua);	
	// debug_printf("%s %d phiub	%d\n\r",__FILE__,__LINE__,phiub);	
	// debug_printf("%s %d phiuc	%d\n\r",__FILE__,__LINE__,phiuc);	
	// debug_printf("%s %d nuab		%f\n\r",__FILE__,__LINE__,nuab);	
	// debug_printf("%s %d nubc		%f\n\r",__FILE__,__LINE__,nubc);	
	// debug_printf("%s %d nuac		%f\n\r",__FILE__,__LINE__,nuac);

	if(nuab < const_u) res+=1;
	if(nubc < const_u) res+=1;
	if(nuac < const_u) res+=1;

	if(res>1)
	{	
		loc_prm->value.val_int = 1;
		return 0;
	}
	loc_prm->value.val_int = 0;
	return 0;
}// calc_break_net1
//****************************************************************************************************
// Активная мощность Сети2
int8_t calc_p_net2(void* val)
{
	float ua = 0, ub = 0, ia = 0, ib = 0;
	int32_t phiua = 0,phiub = 0, phiia = 0, phiic = 0;
	int32_t delta_aui = 0, delta_bui = 0;

	TParam *loc_prm = (TParam*)val;
	
	ua = param[N2UAB].value.val_f;
	ub = param[N2UBC].value.val_f;
	ia = param[N2IA].value.val_f;
	ib = param[N2IB].value.val_f;
	phiua = param[N2PHIUA].value.val_int;
	phiub = param[N2PHIUB].value.val_int;
	phiia = param[N2PHIIA].value.val_int;
	phiic = param[N2PHIIC].value.val_int;
/*	
	 debug_printf("%s %d BPHIIA %d\n\r",__FILE__,__LINE__,param[BPHIIA].value.val_int);
	 debug_printf("%s %d BPHIIB %d\n\r",__FILE__,__LINE__,param[BPHIIB].value.val_int);
	 debug_printf("%s %d BPHIIC %d\n\r",__FILE__,__LINE__,param[BPHIIC].value.val_int);
	 debug_printf("%s %d N2UA %f\n\r",__FILE__,__LINE__,ua);
	 debug_printf("%s %d N2UB %f\n\r",__FILE__,__LINE__,ub);
	 debug_printf("%s %d N2IA %f\n\r",__FILE__,__LINE__,ia);
	 debug_printf("%s %d N2IB %f\n\r",__FILE__,__LINE__,ib);
	 debug_printf("%s %d N2IC %f\n\r",__FILE__,__LINE__,ic);
	 debug_printf("%s %d N2PHIIA %d\n\r",__FILE__,__LINE__,param[N2PHIIA].value.val_int);
	 debug_printf("%s %d N2PHIIB %d\n\r",__FILE__,__LINE__,param[N2PHIIB].value.val_int);
	 debug_printf("%s %d N2PHIIC %d\n\r",__FILE__,__LINE__,param[N2PHIIC].value.val_int);
	 debug_printf("%s %d N2PHIUA %d\n\r",__FILE__,__LINE__,param[N2PHIUA].value.val_int);
	 debug_printf("%s %d N2PHIUB %d\n\r",__FILE__,__LINE__,param[N2PHIUB].value.val_int);
	 debug_printf("%s %d N2PHIUC %d\n\r",__FILE__,__LINE__,param[N2PHIUC].value.val_int);
	 debug_printf("%s %d cosinus(phiua - phiia) %f\n\r",__FILE__,__LINE__,cosinus(phiua - phiia));
	 debug_printf("%s %d cosinus(phiub - phiib) %f\n\r",__FILE__,__LINE__,cosinus(phiub - phiib));
*/	
	
	(phiua>phiia)?(delta_aui=((360-phiua)+phiia)):(delta_aui = phiia-phiua);
	(phiub>phiic)?(delta_bui=((360-phiub)+phiic)):(delta_bui = phiic-phiub);
//	 debug_printf("%s %d cosinus(delta_aui) %f\n\r","kr",__LINE__,cosinus(delta_aui));
//	 debug_printf("%s %d cosinus(delta_bui) %f\n\r","kr",__LINE__,cosinus(delta_bui));

 //   debug_printf("%s %d delta_aui %d delta_bui %d \n\r",__FILE__,__LINE__,delta_aui, delta_bui);
	
	loc_prm->value.val_f = (ua * ia * cosinus(delta_aui) - 
		ub * ib * cosinus(delta_bui))/1000.0;
    if(loc_prm->value.val_f<0)
    {
        loc_prm->value.val_f = (ua * ia * cosinus(delta_aui) - 
          ub * ib * cosinus(delta_bui))/-1000.0;
    }
//	 debug_printf("%s %d loc_prm->value.val_f %f\n\r","kr",__LINE__,loc_prm->value.val_f);

	return 0;
}//end of calc_p_net2
//****************************************************************************************************
// Реактивная мощность Сети2
int8_t calc_q_net2(void* val)
{
	float ua = 0,ub = 0,ia = 0,ic = 0;
	int32_t phiua = 0,phiub = 0,phiia = 0,phiic = 0;
	int32_t delta_aui = 0, delta_bui = 0;

	TParam *loc_prm = (TParam*)val;

	ua = param[N2UAB].value.val_f;
	ub = param[N2UBC].value.val_f;
	//uc = param[N2UAC].value.val_f;
	ia = param[N2IA].value.val_f;
	//ib = param[N2IB].value.val_f;
	ic = param[N2IC].value.val_f;
	phiua = param[N2PHIUA].value.val_int;
	phiub = param[N2PHIUB].value.val_int;
	//phiuc = param[N2PHIUC].value.val_int;
	phiia = param[N2PHIIA].value.val_int;
	//phiib = param[N2PHIIB].value.val_int;
	phiic = param[N2PHIIC].value.val_int;
/*	
    debug_printf("%s %d BPHIIA %d\n\r",__FILE__,__LINE__,param[BPHIIA].value.val_int);
	debug_printf("%s %d BPHIIB %d\n\r",__FILE__,__LINE__,param[BPHIIB].value.val_int);
	debug_printf("%s %d BPHIIC %d\n\r",__FILE__,__LINE__,param[BPHIIC].value.val_int);
	debug_printf("%s %d N2UA %f\n\r",__FILE__,__LINE__,ua);
	debug_printf("%s %d N2UB %f\n\r",__FILE__,__LINE__,ub);
	debug_printf("%s %d N2IA %f\n\r",__FILE__,__LINE__,ia);
	debug_printf("%s %d N2IB %f\n\r",__FILE__,__LINE__,ib);
	debug_printf("%s %d N2IC %f\n\r",__FILE__,__LINE__,ic);
	debug_printf("%s %d N2PHIIA %d\n\r",__FILE__,__LINE__,param[N2PHIIA].value.val_int);
	debug_printf("%s %d N2PHIIB %d\n\r",__FILE__,__LINE__,param[N2PHIIB].value.val_int);
	debug_printf("%s %d N2PHIIC %d\n\r",__FILE__,__LINE__,param[N2PHIIC].value.val_int);
	debug_printf("%s %d N2PHIUA %d\n\r",__FILE__,__LINE__,param[N2PHIUA].value.val_int);
	debug_printf("%s %d N2PHIUB %d\n\r",__FILE__,__LINE__,param[N2PHIUB].value.val_int);
	debug_printf("%s %d N2PHIUC %d\n\r",__FILE__,__LINE__,param[N2PHIUC].value.val_int);
	debug_printf("%s %d cosinus(phiua - phiia) %f\n\r",__FILE__,__LINE__,cosinus(phiua - phiia));
	debug_printf("%s %d cosinus(phiub - phiib) %f\n\r",__FILE__,__LINE__,cosinus(phiub - phiib));
*/
	
	(phiua>phiia)?(delta_aui=((360-phiua)+phiia)):(delta_aui = phiia-phiua);
	(phiub>phiic)?(delta_bui=((360-phiub)+phiic)):(delta_bui = phiic-phiub);
 //   debug_printf("%s %d delta_aui %d delta_bui %d \n\r",__FILE__,__LINE__,delta_aui, delta_bui);

	loc_prm->value.val_f = (ua * ia * cosinus(90-(delta_aui)) -
		 ub * ic * cosinus(90-(delta_bui)))/1000.0;
//	 debug_printf("%s %d loc_prm->value.val_f %f\n\r","kr",__LINE__,loc_prm->value.val_f);
	//loc_prm->value.val_f = (ua * ia * cosinus(90-(phiua - phiia)) -
	//	 ub * ic * cosinus(90-(phiub - phiic)))/1000.0;

	return 0;
}

// Полная мощность Сети2
int8_t calc_s_net2(void* val)
{
	float np, nq;

	TParam *loc_prm = (TParam*)val;

	np = param[N2P].value.val_f;
	nq = param[N2Q].value.val_f;

	loc_prm->value.val_f = sqrtf(np * np + nq * nq);

	return 0;
}

// Косинус Сети2
int8_t calc_cos_net2(void* val)
{
	float np, ns; uint8_t n2cont;

	TParam *loc_prm = (TParam*)val;

    read_data_element(N2_CONT, &n2cont, 4);	
	np = param[N2P].value.val_f;
	ns = param[N2S].value.val_f;

  if(n2cont==1) loc_prm->value.val_f = (ns < 0.1) ? 1: np/ns;
  if(n2cont==0) loc_prm->value.val_f = 0.0;

	return 0;
}
//****************************************************************************************************
// Неверная фазировка Сети2
// 0 - фазировка в норме; 1 - неверная фазировка 
int8_t calc_incorrect_net2(void* val)
{
	int32_t delta_phiab = 0, delta_phibc = 0;
	int32_t phiua = 0, phiub = 0, phiuc = 0;
	float nuab = 0, nubc = 0,  nuac = 0, set_282_uhigh = 0, set_283_umin = 0;
	
	TParam *loc_prm = (TParam*)val;

	phiua = param[N2PHIUA].value.val_int;
	phiub = param[N2PHIUB].value.val_int;
	phiuc = param[N2PHIUC].value.val_int;
	nuab = param[N2UAB].value.val_f;
	nubc = param[N2UBC].value.val_f;
	nuac = param[N2UAC].value.val_f;
	
	read_data_element(s_282, &set_282_uhigh, sizeof(set_282_uhigh));
	read_data_element(s_283, &set_283_umin, sizeof(set_283_umin));
	
		
	// debug_printf("N2PHIUA %d\n\r",param[N2PHIUA].value.val_int);
	// debug_printf("N2PHIUB %d\n\r",param[N2PHIUB].value.val_int);	
	// debug_printf("N2PHIUC %d\n\r",param[N2PHIUC].value.val_int);
	
	if( (nuab>set_283_umin) && (nuab<set_282_uhigh) &&
		(nubc>set_283_umin) && (nubc<set_282_uhigh)	&&
		(nuac>set_283_umin) && (nuac<set_282_uhigh))
		{// если амлитуда напряжения в норме, то смотрим фазы	
	
			(phiua > phiub)?(delta_phiab = (360 - phiua)+phiub):(delta_phiab = phiub - phiua);
			(phiub > phiuc)?(delta_phibc = (360 - phiub)+phiuc):(delta_phibc = phiuc - phiub);
	
			// debug_printf("%s %d delta_phiab %d, delta_phibc %d \n\r",__FILE__, __LINE__, delta_phiab, delta_phibc);
	
			if(((delta_phiab < (120+10)) && (delta_phiab>(120-10))))
			{	
				loc_prm->value.val_int = 0;
			}
			else
			{
			loc_prm->value.val_int = 1;
			}
		}	
	return 0;
}//calc_incorrect_net2
//****************************************************************************************************
/** @details Обрыв фаз Сети2. В текущей версии решил сделать обрыв фаз по напряжению.
*	@return 0 - нет обрыва фаз. 1 - есть обрыв фаз.
*/
int8_t calc_break_net2(void* val)
{
	float nuab = 0, nubc = 0, nuac = 0, const_u = 280.0; // 280 - MAGIC VALUE!
	uint32_t res = 0;

	TParam *loc_prm = (TParam*)val;

	// uint32_t phiua = param[N2PHIUA].value.val_int;
	// uint32_t phiub = param[N2PHIUB].value.val_int;
	// uint32_t phiuc = param[N2PHIUC].value.val_int;
	nuab = param[N2UAB].value.val_f;
	nubc = param[N2UBC].value.val_f;
	nuac = param[N2UAC].value.val_f;
	
	// debug_printf("%s %d phiua	%d\n\r",__FILE__,__LINE__,phiua);	
	// debug_printf("%s %d phiub	%d\n\r",__FILE__,__LINE__,phiub);	
	// debug_printf("%s %d phiuc	%d\n\r",__FILE__,__LINE__,phiuc);	
	// debug_printf("%s %d n2uab	%d\n\r",__FILE__,__LINE__,nuab);	
	// debug_printf("%s %d n2ubc	%d\n\r",__FILE__,__LINE__,nubc);	
	// debug_printf("%s %d n2uac	%d\n\r",__FILE__,__LINE__,nuac);

	if(nuab < const_u) res+=1;			
	if(nubc < const_u) res+=1;
	if(nuac < const_u) res+=1;

	if(res>1)
	{	
		loc_prm->value.val_int = 1;
		return 0;
	}
	loc_prm->value.val_int = 0;
	return 0;
}// end of calc_break_net2

int8_t calc_nnorm(void *val)
{
	TParam *loc_prm = (TParam*)val;

	// Сеть в норме - вернуть 1, иначе 0, независимо от причины
	(param[loc_prm->addrr].value.val_int == net_norm) ? (loc_prm->value.val_int = 1) : (loc_prm->value.val_int = 0);

	return 0;
}// End of calc_nnorm
//****************************************************************************************************
// Активная мощность ЭА
int8_t calc_p_ea(void* val)
{
	float ua = 0, ub = 0, ia = 0, ib = 0;
	int32_t phiua = 0,phiub = 0, phiia = 0, phiic = 0;
	int32_t delta_aui = 0, delta_bui = 0;

	TParam *loc_prm = (TParam*)val;
	
	ua = param[EAUAB].value.val_f;
	ub = param[EAUBC].value.val_f;
	ia = param[EAIA].value.val_f;
	ib = param[EAIB].value.val_f;
	phiua = param[EAPHIUA].value.val_int;
	phiub = param[EAPHIUB].value.val_int;
	phiia = param[EAPHIIA].value.val_int;
	//phiib = param[EAPHIIB].value.val_int;
	phiic = param[EAPHIIC].value.val_int;
/*	
	 debug_printf("%s %d EAIA %f\n\r",__FILE__,__LINE__,ia);
	 debug_printf("%s %d EAIB %f\n\r",__FILE__,__LINE__,ib);
	 debug_printf("%s %d EAPHIUA %d\n\r",__FILE__,__LINE__,param[EAPHIUA].value.val_int);
	 debug_printf("%s %d EAPHIUB %d\n\r",__FILE__,__LINE__,param[EAPHIUB].value.val_int);
	 debug_printf("%s %d EAPHIUC %d\n\r",__FILE__,__LINE__,param[EAPHIUC].value.val_int);
	 debug_printf("%s %d EAPHIIA %d\n\r",__FILE__,__LINE__,param[EAPHIIA].value.val_int);
	 debug_printf("%s %d EAPHIIB %d\n\r",__FILE__,__LINE__,param[EAPHIIB].value.val_int);
	 debug_printf("%s %d EAPHIIC %d\n\r",__FILE__,__LINE__,param[EAPHIIC].value.val_int);
*/	// debug_printf("%s %d cosinus(phiua - phiia) %f\n\r",__FILE__,__LINE__,cosinus(phiua - phiia));
	// debug_printf("%s %d cosinus(phiub - phiib) %f\n\r",__FILE__,__LINE__,cosinus(phiub - phiib));
	
	
	(phiua>phiia)?(delta_aui=((360-phiua)+phiia)):(delta_aui = phiia-phiua);
	(phiub>phiic)?(delta_bui=((360-phiub)+phiic)):(delta_bui = phiic-phiub);
//	 debug_printf("%s %d cosinus(delta_aui) %f\n\r","kr",__LINE__,cosinus(delta_aui));
//	 debug_printf("%s %d cosinus(delta_bui) %f\n\r","kr",__LINE__,cosinus(delta_bui));
	
//	 debug_printf("%s %d delta_aui %d delta_bui %d \n\r",__FILE__,__LINE__,delta_aui, delta_bui);
	
	loc_prm->value.val_f = (ua * ia * cosinus(delta_aui) - 
		ub * ib * cosinus(delta_bui))/1000.0;
		//my_debug
    //if(loc_prm->value.val_f<0)
    //{
    //    loc_prm->value.val_f = (ua * ia * cosinus(delta_aui) - 
    //      ub * ib * cosinus(delta_bui))/-1000.0;
    //}
//	 debug_printf("%s %d loc_prm->value.val_f %f\n\r","kr",__LINE__,loc_prm->value.val_f);

  return 0;
}//calc_p_ea
//****************************************************************************************************
// Реактивная мощность ЭА
int8_t calc_q_ea(void* val)
{
	float ua=0,ub=0,ia=0,ic=0;
	int32_t phiua=0,phiub=0,phiia=0,phiic=0;
	int32_t delta_aui = 0, delta_bui = 0;

	TParam *loc_prm = (TParam*)val;

	ua = param[EAUAB].value.val_f;
	ub = param[EAUBC].value.val_f;
	ia = param[EAIA].value.val_f;
	ic = param[EAIC].value.val_f;
	phiua = param[EAPHIUA].value.val_int;
	phiub = param[EAPHIUB].value.val_int;
	phiia = param[EAPHIIA].value.val_int;
	//phiib = param[EAPHIIB].value.val_int;
	phiic = param[EAPHIIC].value.val_int;

	(phiua>phiia)?(delta_aui=((360-phiua)+phiia)):(delta_aui = phiia-phiua);
	(phiub>phiic)?(delta_bui=((360-phiub)+phiic)):(delta_bui = phiic-phiub);

	loc_prm->value.val_f = (ua * ia * cosinus(90-(delta_aui)) -
		 ub * ic * cosinus(90-(delta_bui)))/1000.0;
//	 debug_printf("%s %d loc_prm->value.val_f %f\n\r","kr",__LINE__,loc_prm->value.val_f);
//    loc_prm->value.val_f = (ua * ia * cosinus(90-(phiua - phiia)) -
//		 ub * ic * cosinus(90-(phiub - phiic)))/1000.0;

	return 0;
}// end of calc_q_ea
//****************************************************************************************************
// Полная мощность ЭА
int8_t calc_s_ea(void* val)
{
	float eap, eaq;

	TParam *loc_prm = (TParam*)val;

	eap = param[EAP].value.val_f;
	eaq = param[EAQ].value.val_f;

	loc_prm->value.val_f = sqrtf(eap * eap + eaq * eaq);

	return 0;
}
//****************************************************************************************************
// Косинус ЭА
int8_t calc_cos_ea(void* val)
{
	float eap, eas; uint8_t eacont;

	TParam *loc_prm = (TParam*)val;

    read_data_element(EA_CONT, &eacont, 4);	
	eap = param[EAP].value.val_f;
	eas = param[EAS].value.val_f;

  if(eacont==1) loc_prm->value.val_f = (eas < 0.1) ? 1: eap/eas;
  if(eacont==0) loc_prm->value.val_f = 0.0;

	return 0;
}
//****************************************************************************************************
int8_t calc_ea_p_oil(void* val)
{
	
	TParam *loc_prm = (TParam*)val;
	
	
	loc_prm->value.val_int = param[loc_prm->addrr].val_i;
	
	return 0;
}
//****************************************************************************************************
int8_t calc_ea_p_oil_new(void* val)
{
	float p, p_oil_min, p_oil_max;
	 
	TParam *loc_prm = (TParam*)val;
	
	loc_prm->value.val_int = param[loc_prm->addrr].val_i;
	
	p = param[EAPOIL].value.val_f;
	
	p_oil_min = preset[s_43_].cur_value.val_f;
	
	p_oil_max = preset[s_219_].cur_value.val_f;	
	
	
	if (p<=p_oil_max && p>p_oil_min)
	{ 
		loc_prm->value.val_int = 1; 
		
	}
	else
	{
		loc_prm->value.val_f = 0;
		
	}
		
	return 0;
}
 // Расчет времени наработки ЭА
int8_t calc_motohours(void* val)
{
	static uint8_t flag = 0;

	TParam *loc_prm = (TParam*)val;

	if ((ea.state == dg_on) || (ea.state == dg_gpn))
	{
		// ЭА запущен
		flag = 1;
		// Добавляем к значению 10 секунд
		loc_prm->value.val_int += 10;
	}
	else
	{
		// ЭА не запущен
		if (flag)
		{
			// Добавляем к значению 5 секунд, т.к. не знаем точное время останова ЭА
			loc_prm->value.val_int += 5;
			// ЭА только что был запущен, сообщаем задаче о необходимости записи
			mutex_signal(&motohours_mutex, NULL);
		}
		// Сбросить флаг
		flag = 0;
	}

	return 0;
}
// Расчет времени наработки в часах
int8_t calc_hours(void* val)
{
	//uint32_t sec = param[loc_prm->addrr].value.val_int;
	
	TParam *loc_prm = (TParam*)val;
	
	loc_prm->value.val_int = param[loc_prm->addrr].value.val_int/3600;
	//debug_printf("%s %d calc_station_hours\n\r", "params.c", __LINE__);
	return 0;
}
// Расчет времени наработки ЭА с перегрузом в пределах 10 %
int8_t calc_motohours10(void* val)
{
	 static uint8_t flag = 0;

	 TParam *loc_prm = (TParam*)val;

	// Считаем наработку, если хотя бы один порог сработал
	 if (limit[LIMPEA].flag || limit[LIMPEA].flag || limit[LIMPEA].flag)
	 {
		 // Есть перегруз
		 flag = 1;
		 // Добавляем к значению 10 секунд
		 loc_prm->value.val_int += 10;
	 }
	 else
	 {
		 // Нет перегруза
		 if (flag)
		 {
			 // Добавляем к значению 5 секунд
			 loc_prm->value.val_int += 5;
			 // Перегруз только что был, сообщаем задаче о необходимости записи
			 mutex_signal(&motohours_mutex, NULL);
		 }
		 // Сбросить флаг
		 flag = 0;
	 }

	return 0;
}// end of calc_motohours10
// Расчет времени, оставшегося до ТО ЭА
int8_t calc_motohours_left(void* val)
{
	TParam *loc_prm = (TParam*)val;

	// Проверяем признак "Требуется ТО ЭА"
	if (motohours_data.attribs.need_service_ea)
	{
		// требуется, записать 0
		loc_prm->value.val_int = 0;
	}
	else
	{
		// Разность больше уставки?
		if ((param[EAMOTOHOURS].value.val_int - motohours_data.ea_service_time) >= (preset[s_160_].cur_value.val_int / 1000))
		{
			// период ТО истек, выставить признак
			motohours_data.attribs.need_service_ea = 1;
			// обнулить параметр
			loc_prm->value.val_int = 0;
		}
		else
		{
			// не истек, вычесть 60 секунд
			//loc_prm->value.val_int -= 60;
			loc_prm->value.val_int = (preset[s_160_].cur_value.val_int / 1000) - param[EAMOTOHOURS].value.val_int + motohours_data.ea_service_time;
			// на всякий случай
			if (((int32_t)(loc_prm->value.val_int)) < 0)
			{
				loc_prm->value.val_int = 0;
			}
		}
	}

	return 0;
}
 // Расчет времени наработки ПЧ1
int8_t calc_fc1_motohours(void* val)
{
	static uint8_t flag = 0;
    uint32_t fc1state = 0;
	
    TParam *loc_prm = (TParam*)val;

	read_data_element(FC1_AE_STATE, &fc1state, 4);	
	
    if ((fc1state != 0) && (fc1state != 2))
	{
		// ПЧ запущен
		flag = 1;
		// Добавляем к значению 10 секунд
		loc_prm->value.val_int += 10;
	}
	else
	{
		// ПЧ не запущен
		if (flag)
		{
			// Добавляем к значению 120 секунд это время инерции останова ПЧ 
			loc_prm->value.val_int += 120;
			// ПЧ только что был запущен, сообщаем задаче о необходимости записи
			mutex_signal(&motohours_mutex, NULL);
		}
		// Сбросить флаг
		flag = 0;
	}

	return 0;
}
 // Расчет времени наработки ПЧ2
int8_t calc_fc2_motohours(void* val)
{
	static uint8_t flag = 0;
    uint32_t fc2state = 0;
	
    TParam *loc_prm = (TParam*)val;

	read_data_element(FC2_AE_STATE, &fc2state, 4);	
	
    if ((fc2state != 0) && (fc2state != 2))
	{
		// ПЧ запущен
		flag = 1;
		// Добавляем к значению 10 секунд
		loc_prm->value.val_int += 10;
	}
	else
	{
		// ПЧ не запущен
		if (flag)
		{
			// Добавляем к значению 120 секунд это время инерции останова ПЧ 
			loc_prm->value.val_int += 120;
			// ПЧ только что был запущен, сообщаем задаче о необходимости записи
			mutex_signal(&motohours_mutex, NULL);
		}
		// Сбросить флаг
		flag = 0;
	}

	return 0;
}
//****************************************************************************************************
// Отслеживание потока старта
int8_t calc_is_start_mode(void)
{
    if(start_task) 
        return !(list_is_empty(&start_task->item));
    else return 0;
}
// Отслеживание потока стопа
int8_t calc_is_stop_mode(void)
{
    if(stop_task) 
        return !(list_is_empty(&stop_task->item));
    else return 0;
}
// Отслеживание потоков старта и стопа режима работы источнков
int8_t calc_unit_control_3(void* val)
{
  TParam *loc_prm = (TParam*)val;
    
  uint32_t source_modes = 0; 
    
  read_data_element(SOURCE_MODES, &source_modes, 4);	
  if(source_modes == 0)
  {
    if(calc_is_stop_mode()) 
      loc_prm->value.val_int = 4;
    else
      loc_prm->value.val_int = 0;
  }  
  else
  {
    if(calc_is_start_mode()) 
      loc_prm->value.val_int = 1;
    else  
      loc_prm->value.val_int = 2;

  }  
     
    return 0;
}
//****************************************************************************************************
// Контроль за авариями по уровню толпива
int8_t calc_control_alarm_level(void* val)
{
	TParam *loc_prm = (TParam*)val;
    
    if(alarm[EA354_].state ==1 && alarm[EA355_].state ==1)
        loc_prm->value.val_int = 1; 
    else loc_prm->value.val_int = 0;  
    
    return 0;
}
//****************************************************************************************************
// Вычисление сырого значение корректора напряжения
int8_t calc_corrector_value(void* val)
{
	TParam *loc_prm = (TParam*)val;
    
    loc_prm->value.val_int = get_volt_mod420(); 
    
    return 0;
}
//****************************************************************************************************
// Расчет SOURCE_MODES
int8_t calc_source_modes(void* val)
{
	TParam *loc_prm = (TParam*)val;
    	
    loc_prm->value.val_int = main_config_file.nbm_current_mode; 

    return 0;
}
//****************************************************************************************************
// Команды БУ 50
int8_t make_commands(void* val)
{
	uint32_t tmp_val = 0;

	TParam *loc_prm = (TParam*)val;

	// Бит 1 - CONT_NET
	tmp_val |= (cont[CONTNET].state && 0x01) << 		0;
	// Бит 2 - CONT_NET2
	tmp_val |= (cont[CONTNET2].state && 0x01) << 		1;
	// Бит 3 - CONT_EA
	tmp_val |= (cont[CONTEA].state && 0x01) << 			2;
	// Бит 4 - STARTER_EA
	tmp_val |= (cont[STARTEREA].state && 0x01) <<		3;
	// Бит 5 - ASU_EA
	tmp_val |= (cont[ASUEA].state && 0x01) << 			4;
	// Бит 6 - CONT_MKI
	tmp_val |= (cont[CONTMKI].state && 0x01) << 		5;
	// Бит 7 - ANCHOR_STARTER_EA
	tmp_val |= (cont[ANCHORSTARTEREA].state && 0x01) << 6;
	// Бит 8 - FIELD_START
	tmp_val |= (cont[FIELDSTART].state && 0x01) << 		7;

	// Бит 9 - FUEL_TOGGLE
	tmp_val |= (cont[FUELTOGGLE].state && 0x01) << 	8;
	// Бит 10 - CONT_EN
	tmp_val |= (cont[CONTEN].state && 0x01) << 		9;
	// Бит 11 - CONT_EN_OIL
	tmp_val |= (cont[CONTENOIL].state && 0x01) << 	10;
	// Бит 12 - CONT_FID3
	tmp_val |= (cont[CONTFID3].state && 0x01) << 	11;
	// Бит 13 - CONT_FID3_1
	tmp_val |= (cont[CONTFID31].state && 0x01) << 	12;
	// Бит 14 - CONT_FID3_2
	tmp_val |= (cont[CONTFID32].state && 0x01) << 	13;
	// Бит 15 - CONT_FID4
	tmp_val |= (cont[CONTFID4].state && 0x01) << 	14;
	// Бит 16 - CONT_VENT
	tmp_val |= (cont[CONTVENT].state && 0x01) << 	15;

	// Бит 17 - CONT_FID1
	tmp_val |= (cont[CONTFID1].state && 0x01) << 		16;
	// Бит 18 - CONT_FID2
	tmp_val |= (cont[CONTFID2].state && 0x01) << 		17;
	// Бит 19 - HATCH_5_O
	tmp_val |= (cont[HATCH5O].state && 0x01) << 		18;
	// Бит 20 - HATCH_5_C
	tmp_val |= (cont[HATCH5C].state && 0x01) << 		19;
	// Бит 21 - HATCH_6_O
	tmp_val |= (cont[HATCH6O].state && 0x01) << 		20;
	// Бит 22 - HATCH_6_C
	tmp_val |= (cont[HATCH6C].state && 0x01) << 		21;
	// Бит 23 - CONT_AE_FC1
	tmp_val |= (cont[CONTAEFC1].state && 0x01) << 		22;
	// Бит 24 - CONT_AE_FC1_TRIANGLE
	tmp_val |= (cont[CONTAEFC1TRIANGLE].state && 0x01) << 23;

	// Бит 25 - CONT_AE_FC1_STAR
	tmp_val |= (cont[CONTAEFC1STAR].state && 0x01) << 		24;
	// Бит 26 - CONT_AE_FC2
	tmp_val |= (cont[CONTAEFC2].state && 0x01) << 			25;
	// Бит 27 - CONT_AE_FC2_TRIANGLE
	tmp_val |= (cont[CONTAEFC2TRIANGLE].state && 0x01) << 	26;
	// Бит 28 - CONT_AE_FC2_STAR
	tmp_val |= (cont[CONTAEFC2STAR].state && 0x01) << 		27;
	// Биты 29-31 - резерв

	// Записать значение
	loc_prm->value.val_int = tmp_val;

	return 0;
}// End of make_commands

// Донесения1 БУ 50
int8_t make_reports1(void* val)
{
	uint32_t tmp_val = 0;

	TParam *loc_prm = (TParam*)val;

	// Бит 0 - RBP
	tmp_val |= (param[RBP_].value.val_int)			<< 0;
	// Бит 1 - N_CONT
	tmp_val |= (param[NCONT].value.val_int) 		<< 1;
	// Бит 2 - N2_CONT
	tmp_val |= (param[N2CONT].value.val_int)		<< 2;
	// Бит 3 - EA_CONT
	tmp_val |= (param[EACONT].value.val_int) 		<< 3;
	// Бит 4 - EA_COOL_NORM
	tmp_val |= (param[EACOOLNORM].value.val_int) 	<< 4;
	// Бит 5 - EA_FILTER_NORM
	tmp_val |= (param[EAFILTERNORM].value.val_int) 	<< 5;
	// Бит 6 - B_MKI_ON
	tmp_val |= (param[BMKION].value.val_int)		<< 6;
	// Бит 7 - B_MKI_AI
	tmp_val |= (param[BMKIAI].value.val_int)		<< 7;

	// Бит 8 - CHARGE_GEN
	tmp_val |= (param[CHARGEGEN].value.val_int)				<< 8;
	// Бит 9 - T_GEN_NORM
	tmp_val |= (param[TGENNORM].value.val_int) 				<< 9;
	// Бит 10 - T_BEARING_NORM
	tmp_val |= (param[TBEARINGNORM].value.val_int) 			<< 10;
	// Бит 11 - STARTER_FROM_AB_ST_K1
	tmp_val |= (param[STARTERFROMABSTK1].value.val_int) 	<< 11;
	// Бит 12 - STARTER_FROM_AB_SHASSIS_K2
	tmp_val |= (param[STARTERFROMABSHASSISK2].value.val_int) << 12;
	// Бит 13 - EN_AUT
	tmp_val |= (param[ENAUT].value.val_int) 				<< 13;
	// Бит 14 - EN_CONT
	tmp_val |= (param[ENCONT].value.val_int) 				<< 14;
	// Бит 15 - EN_AUT_OP
	tmp_val |= (param[ENAUTOP].value.val_int) 				<< 15;

	// Бит 16 - EN_PROTECTION
	tmp_val |= (param[ENPROTECTION].value.val_int)	<< 16;
	// Бит 17 - FID3_AUT
	tmp_val |= (param[FID3AUT].value.val_int) 		<< 17;
	// Бит 18 - FID3_AUT_OP
	tmp_val |= (param[FID3AUTOP].value.val_int) 	<< 18;
	// Бит 19 - FID3_CONT
	tmp_val |= (param[FID3CONT].value.val_int)		<< 19;
	// Бит 20 - FID3_1_AUT
	tmp_val |= (param[FID31AUT].value.val_int) 		<< 20;
	// Бит 21 - FID3_1_AUT_OP
	tmp_val |= (param[FID31AUTOP].value.val_int) 	<< 21;
	// Бит 22 - FID3_1_CONT
	tmp_val |= (param[FID31CONT].value.val_int)		<< 22;
	// Бит 23 - FID3_2_AUT
	tmp_val |= (param[FID32AUT].value.val_int) 		<< 23;

	// Бит 24 - FID3_2_AUT_OP
	tmp_val |= (param[FID32AUTOP].value.val_int) 	<< 24;
	// Бит 25 - FID3_2_CONT
	tmp_val |= (param[FID32CONT].value.val_int) 	<< 25;
	// Бит 26 - FID4_AUT
	tmp_val |= (param[FID4AUT].value.val_int) 		<< 26;
	// Бит 27 - FID4_AUT_OP
	tmp_val |= (param[FID4AUTOP].value.val_int) 	<< 27;
	// Бит 28 - FID4_CONT
	tmp_val |= (param[FID4CONT].value.val_int) 		<< 28;
	// Бит 29 - TRANS_AUT, Q5
	tmp_val |= (param[TRANSAUT].value.val_int) 		<< 29;
	// Бит 30 - TRANS_AUT_OP, Q5
	tmp_val |= (param[TRANSAUTOP].value.val_int) 	<< 30;
	// Бит 31 - TRANS2_AUT, Q6
	tmp_val |= (param[TRANS2AUT].value.val_int) 	<< 31;

	// Записать значение
	loc_prm->value.val_int = tmp_val;

	return 0;
}// End of make_reports1

// Донесения2 БУ 50
int8_t make_reports2(void* val)
{
	uint32_t tmp_val = 0;

	TParam *loc_prm = (TParam*)val;

	// Бит 0 - TRANS2_AUT_OP
	tmp_val |= (param[TRANS2AUTOP].value.val_int)	<< 0;
	// Бит 1 - VENT_CONT
	tmp_val |= (param[VENTCONT].value.val_int)		<< 1;
	// Бит 2 - FID1_AUT
	tmp_val |= (param[FID1AUT].value.val_int) 		<< 2;
	// Бит 3 - FID1_AUT_OP
	tmp_val |= (param[FID1AUTOP].value.val_int) 	<< 3;
	// Бит 4 - FID1_CONT
	tmp_val |= (param[FID1CONT].value.val_int) 		<< 4;
	// Бит 5 - FID2_CONT
	tmp_val |= (param[FID2CONT].value.val_int) 		<< 5;
	// Бит 6 - VENT_MANUAL
	tmp_val |= (param[VENTMANUAL].value.val_int) 	<< 6;
	// Бит 7 - VENT_AUTOMATIC
	tmp_val |= (param[VENTAUTOMATIC].value.val_int) << 7;

	// Бит 8 - EN_OIL_CONT
	tmp_val |= (param[ENOILCONT].value.val_int)	<< 8;
	// Бит 9 - O_H_5
	tmp_val |= (param[OH5].value.val_int) 		<< 9;
	// Бит 10 - C_H_5
	tmp_val |= (param[CH5].value.val_int) 		<< 10;
	// Бит 11 - ON_O_H_5
	tmp_val |= (param[ONOH5].value.val_int) 	<< 11;
	// Бит 12 - ON_C_H_5
	tmp_val |= (param[ONCH5].value.val_int) 	<< 12;
	// Бит 13 - O_H_6
	tmp_val |= (param[OH6].value.val_int) 		<< 13;
	// Бит 14 - C_H_6
	tmp_val |= (param[CH6].value.val_int) 		<< 14;
	// Бит 15 - ON_O_H_6
	tmp_val |= (param[ONOH6].value.val_int) 	<< 15;

	// Бит 16 - ON_C_H_6
	tmp_val |= (param[ONCH6].value.val_int) 			<< 16;
	// Бит 17 - AE_FC1_CONT, KM3 ПЧ1
	tmp_val |= (param[AEFC1CONT].value.val_int) 			<< 17;
	// Бит 18 - AE_FC1_TRIANGLE_CONT, КМ5 ПЧ1
	tmp_val |= (param[AEFC1TRIANGLECONT].value.val_int) 	<< 18;
	// Бит 19 - AE_FC1_STAR_CONT
	tmp_val |= (param[AEFC1STARCONT].value.val_int) 		<< 19;
	// Бит 20 - AE_FC2_CONT
	tmp_val |= (param[AEFC2CONT].value.val_int) 		<< 20;
	// Бит 21 - AE_FC2_TRIANGLE_CONT
	tmp_val |= (param[AEFC2TRIANGLECONT].value.val_int) << 21;
	// Бит 22 - AE_FC2_STAR_CONT
	tmp_val |= (param[AEFC2STARCONT].value.val_int) 	<< 22;
	// Бит 23 - LOW_FUEL
	tmp_val |= (param[LOWFUEL].value.val_int)  		    << 23;

	// Бит 24 - LOW_EXT_FUEL
	tmp_val |= (param[LOWEXTFUEL].value.val_int)		<< 24;
	// Биты 8, 26-31 - резерв
	tmp_val |= (param[PROTECTIONSSTATE].value.val_int)	<< 25;
	
	// Записать значение
	loc_prm->value.val_int = tmp_val;

	return 0;
}// End of make_reports2

int8_t make_alarms_ea(void* val)
{
	uint32_t tmp_val = 0;

	TParam *loc_prm = (TParam*)val;
	
	tmp_val |= (alarm[EA000_].state);
	tmp_val |= (alarm[EA001_].state)<<	1;
	tmp_val |= (alarm[EA002_].state)<<	2;
	tmp_val |= (alarm[EA003_].state)<<	3;
	tmp_val |= (alarm[EP304_].state)<<	4;
	tmp_val |= (alarm[EA005_].state)<<	5;
	tmp_val |= (alarm[EP007_].state)<<	6;
	tmp_val |= (alarm[EA007_].state)<<	7;
//
	tmp_val |= (alarm[EA008_].state)<<	8;	
	tmp_val |= (alarm[EA009_].state)<<	9;
	tmp_val |= (alarm[EA010_].state)<<	10;
	tmp_val |= (alarm[EP003_].state)<<	11;
	tmp_val |= (alarm[EA012_].state)<<	12;	
	tmp_val |= (alarm[EA100_].state)<<	13;
	tmp_val |= (alarm[EA101_].state)<<	14;
	tmp_val |= (alarm[EA102_].state)<<	15;
//
	tmp_val |= (alarm[EA103_].state)<<	16;	
	tmp_val |= (alarm[EA106_].state)<<	17;	
	tmp_val |= (alarm[EA108_].state)<<	18;
	tmp_val |= (alarm[EA110_].state)<<	19;
	
	tmp_val |= (alarm[EA111_].state)<<	20;
	tmp_val |= (alarm[EA344_].state)<<	21;
	tmp_val |= (alarm[EA345_].state)<<	22;
	tmp_val |= (alarm[EP001_].state)<<	23;
//
	tmp_val |= (alarm[EA107_].state)<<	24;	
	tmp_val |= (alarm[EP109_].state)<<	25;	
	tmp_val |= (alarm[EA326_].state)<<	26;	
	tmp_val |= (alarm[EA112_].state)<<	27;
	tmp_val |= (0)<<					28;
	tmp_val |= (0)<<					29;
	tmp_val |= (0)<<					30;
	tmp_val |= (0)<<					31;
	
	// Записать значение
	loc_prm->value.val_int = tmp_val;
	return 0;
}// end of make_alarms_ea

//******************************************************************************************
int8_t make_events_net(void *val)
{
	uint32_t tmp_val = 0;

	TParam *loc_prm = (TParam*)val;
	
	tmp_val	= (alarm[EA200_].state);
	tmp_val	|= (alarm[EA201_].state)		<< 1;
	tmp_val	|= (alarm[EA202_].state)		<< 2; 
	tmp_val	|= (alarm[EA203_].state)		<< 3;
	tmp_val	|= (alarm[EA206_].state)		<< 4;	//неисправность контактора сети
	tmp_val	|= (alarm[EA219_].state)		<< 7;	// КЗ сети
	
	
	tmp_val	|= (alarm[EA224_].state)		<< 8;	// Нештатное отключение сети
	tmp_val	|= (alarm[EA204_].state)		<< 9;	// Не норма изоляции от РБП
	tmp_val	|= (alarm[EA207_].state)		<< 10;	// Частота сети ниже нормы
	tmp_val	|= (alarm[EA208_].state)		<< 11;	// Частота сети выше нормы
	
	
	tmp_val	|= (alarm[EP225_].state)		<< 16;	// Перегруз сети по мощности
	tmp_val	|= (alarm[EA322_].state)		<< 17;	// КЗ ЭН
	tmp_val	|= (alarm[EA306_].state)		<< 18;	// Обрыв фазы ЭН
	tmp_val	|= (alarm[EA305_].state)		<< 19;	// Контроль вкл/откл контактора ЭН
	tmp_val	|= (alarm[EA324_].state)		<< 20;	// Контроль КЗ автомата ЭН 
	tmp_val	|= (alarm[EA313_].state)		<< 21;	// Контроль вкл/откл контактора ЭН масла
	tmp_val	|= (alarm[EP324_].state)		<< 22;	// Контроль автомата ЭН 
	
	// Записать значение
	loc_prm->value.val_int = tmp_val;
	
	return 0;
}// end of make_events_net
//****************************************************************************************************

int8_t make_events_net2(void *val)
{
	uint32_t tmp_val = 0;

	TParam *loc_prm = (TParam*)val;
	
	tmp_val	= 	(alarm[EA200_2_].state);
	tmp_val	|= 	(alarm[EA201_2_].state)		<< 1;
	tmp_val	|= 	(alarm[EA202_2_].state)		<< 2; 
	tmp_val	|= 	(alarm[EA203_2_].state)		<< 3;
	tmp_val	|= 	(alarm[EA206_2_].state)		<< 4;
	tmp_val	|= 	(alarm[EA219_2_].state)		<< 7;
	
	
	tmp_val	|= 	(alarm[EA224_2_].state)		<< 8;
	
	tmp_val	|= (alarm[EA207_2_].state)		<< 10;	// Частота сети ниже нормы
	tmp_val	|= (alarm[EA208_2_].state)		<< 11;	// Частота сети выше нормы
	
	tmp_val	|= 	(alarm[EP225_2_].state)		<< 16;
	
	// Записать значение
	loc_prm->value.val_int = tmp_val;
	
	return 0;
}
//****************************************************************************************************
int8_t make_events_fc_50(void* val)
{
	uint32_t tmp_val = 0;

	TParam *loc_prm = (TParam*)val;
	
	tmp_val	= 	(alarm[EA550_1_].state);
	tmp_val	|= 	(alarm[EA551_1_].state)		<< 1;
	tmp_val	|= 	(alarm[EA552_1_].state)		<< 2; 
	tmp_val	|= 	(alarm[EA553_].state)		<< 3;
	tmp_val	|= 	(alarm[EA562_1_].state)		<< 4;
	tmp_val	|= 	(alarm[EA564_1_].state)		<< 5;
	tmp_val	|= 	(alarm[EA563_1_].state)		<< 6;
	tmp_val	|= 	(alarm[EP565_1_].state)		<< 7;
	//
	tmp_val	|= 	(alarm[EA566_1_].state)		<< 8;
    tmp_val	|= 	(alarm[EA550_2_].state)     << 15;
	
    tmp_val	|= 	(alarm[EA551_2_].state)		<< 16;
    tmp_val	|= 	(alarm[EA552_1_].state)		<< 17; 
	tmp_val	|= 	(alarm[EA553_2_].state)		<< 18;
	tmp_val	|= 	(alarm[EA562_2_].state)		<< 19;
	tmp_val	|= 	(alarm[EA564_2_].state)		<< 20;
	tmp_val	|= 	(alarm[EA563_2_].state)		<< 21;
	tmp_val	|= 	(alarm[EP565_2_].state)		<< 22;
	tmp_val	|= 	(alarm[EA566_2_].state)		<< 23;
	

	
	// Записать значение
	loc_prm->value.val_int = tmp_val;
	
	return 0;
}// end of make_events_fc_50
//****************************************************************************************************
int8_t make_events_bu_50(void *val)
{
	uint32_t tmp_val = 0;

	TParam *loc_prm = (TParam*)val;
	
	tmp_val	= (alarm[EA600_].state);				//неисправность контактора вентилятора
	tmp_val	|= (alarm[EA336_].state)		<< 1;
	tmp_val	|= (alarm[EP336_].state)		<< 2;
	tmp_val	|= (alarm[EA337_].state)		<< 3;
	tmp_val	|= (alarm[EP337_].state)		<< 4;
	tmp_val	|= (alarm[EA338_].state)		<< 5;
	tmp_val	|= (alarm[EP338_].state)		<< 6;
	tmp_val	|= (alarm[EA339_].state)		<< 7;
	tmp_val	|= (alarm[EP339_].state)		<< 8;
	tmp_val	|= (alarm[EA346_].state)		<< 9;
	tmp_val	|= (alarm[EP346_].state)		<< 10;
	tmp_val	|= (alarm[EA347_].state)		<< 11;
	tmp_val	|= (alarm[EP347_].state)		<< 12;
	tmp_val	|= (alarm[EA348_].state)		<< 13;
	tmp_val	|= (alarm[EP348_].state)		<< 14;
	
	// Записать значение
	loc_prm->value.val_int = tmp_val;
	
	return 0;
}// end of make_events_bu_50
//****************************************************************************************************
int8_t polling_mav_a4(void* arg)
{
	module[MODULES_50_A4].write_word(&module[MODULES_50_A4], 5, 3);
	return 0;
}//end of polling_mav_a4
//****************************************************************************************************
int8_t polling_mav_a5(void* arg)
{
	module[MODULES_50_A5].write_word(&module[MODULES_50_A5], 5, 3);
	return 0;
}

int8_t polling_mav_a6(void* arg)
{
	module[MODULES_50_A6].write_word(&module[MODULES_50_A6], 5, 3);
	return 0;
}

void init_params_station()
{
	int8_t err = 0;
 
    // Общая наработка станции
	static char parname_STATIONMOTOHOURS[] = "STATION_MOTOHOURS";
	param[STATIONMOTOHOURS].name 	= parname_STATIONMOTOHOURS;
	param[STATIONMOTOHOURS].type 	= PARAM_TYPE_SECOND;
	param[STATIONMOTOHOURS].addrr 	= 0;
	param[STATIONMOTOHOURS].read 	= calc_station_motohours;
	err = param_init(&param[STATIONMOTOHOURS]);
	periodic_add_item(&params_periodic, &param[STATIONMOTOHOURS], param[STATIONMOTOHOURS].name,	100);

    // Наработка всей станции в часах
	static char parname_STATIONHOURS[] = "STATION_HOURS";
	param[STATIONHOURS].name           = parname_STATIONHOURS;
	param[STATIONHOURS].type 	       = PARAM_TYPE_SECOND;
	param[STATIONHOURS].addrr 		   = STATIONMOTOHOURS;
	param[STATIONHOURS].read           = calc_hours;
	err = param_init(&param[STATIONHOURS]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
    periodic_add_item(&params_periodic, &param[STATIONHOURS], param[STATIONHOURS].name, 100);


    // Донесение "РБП"
	static char parname_RBP[] = "RBP";
	init_discrete(RBP_, MODULES_50_A8, DISCR_CH_17, parname_RBP, 1);

    // Отслеживание потоков старта и стопа режима работы источнков
	static char parname_UNITCONTROL3[]  	= "UNIT_CONTROL_3";
	param[UNITCONTROL3].name 				= parname_UNITCONTROL3;
	param[UNITCONTROL3].type 				= PARAM_TYPE_SECOND;
	param[UNITCONTROL3].read 				= calc_unit_control_3;
	err = param_init(&param[UNITCONTROL3]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[UNITCONTROL3], param[UNITCONTROL3].name,	1);
	param[UNITCONTROL3].value.val_int = 0;

    // Режимы включения источников
	static char parname_SOURCEMODES[] = "SOURCE_MODES";
	param[SOURCEMODES].name 	= parname_SOURCEMODES;
	param[SOURCEMODES].type 				= PARAM_TYPE_SECOND;
	param[SOURCEMODES].read 				= calc_source_modes;
	err = param_init(&param[SOURCEMODES]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[SOURCEMODES], param[SOURCEMODES].name,	5);
	param[SOURCEMODES].value.val_int = 0;

    // Отслеживание потоков старта и стопа режима работы источнков
	static char parname_SOURCESSINHR[]  	    = "SOURCES_SINHR";
	param[SOURCESSINHR].name 				= parname_SOURCESSINHR;
	param[SOURCESSINHR].type 				= PARAM_TYPE_EXT_RENEW;
	// значение записывается вышестоящим кодом средствами адаптера данных
	err = param_init(&param[SOURCESSINHR]);

    // Контроль за авариями по уровню топливу
	static char parname_CONTROLALARMLEVEL[] = "CONTROL_ALARM_LEVEL";
	param[CONTROLALARMLEVEL].name 	= parname_CONTROLALARMLEVEL;
	param[CONTROLALARMLEVEL].type 	= PARAM_TYPE_SECOND;
	param[CONTROLALARMLEVEL].addrr 	= 0;
	param[CONTROLALARMLEVEL].read 	= calc_control_alarm_level;
	err = param_init(&param[CONTROLALARMLEVEL]);
	periodic_add_item(&params_periodic, &param[CONTROLALARMLEVEL], param[CONTROLALARMLEVEL].name,	10);

    // Сырое значение корректора напряжения
	static char parname_CORRECTORVALUE[] = "CORRECTOR_VALUE";
	param[CORRECTORVALUE].name 	= parname_CORRECTORVALUE;
	param[CORRECTORVALUE].type 	= PARAM_TYPE_SECOND;
	param[CORRECTORVALUE].read 	= calc_corrector_value;
	err = param_init(&param[CORRECTORVALUE]);
	periodic_add_item(&params_periodic, &param[CORRECTORVALUE], param[CONTROLALARMLEVEL].name,	50);


//	// Пожар
//	FIRE_EXT,
//	// Состояние защит
// Состояние защит
	static char parname_PROTECTIONSSTATE[] = "PROTECTIONS_STATE";
	param[PROTECTIONSSTATE].name 	= parname_PROTECTIONSSTATE;
	param[PROTECTIONSSTATE].type 	= PARAM_TYPE_EXT_RENEW;
	// значение записывается вышестоящим кодом средствами адаптера данных
	err = param_init(&param[PROTECTIONSSTATE]);

}// End of init_params_station

void init_params_net1()
{
	int8_t err = 0;

	// U линейное AB
	static char parname_NUAB[]		= "N_U_AB";
	param[NUAB].name 				= parname_NUAB;
	param[NUAB].type 				= PARAM_TYPE_ANALOG;
	param[NUAB].module 				= &module[MODULES_50_A4];
	param[NUAB].addrr 				= MOD380_ADDR_RMS + MOD380_CH_01;
	param[NUAB].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[NUAB].coef 			= &coefs[N_U_AB_k];
	mas_calibr[NUAB].calibr 		= param_calibr_line_voltage;
	param[NUAB].calibr_obj			= &mas_calibr[NUAB];
	// Фильтр скользящим средним
	param[NUAB].filter_obj.filter_type 		= f_no_filter;// f_moving_average; mydebug_burn
	param[NUAB].filter_obj.filter_ptr.fma	= &N_U_AB_FILTER;
	err = param_init(&param[NUAB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NUAB], param[NUAB].name, 1);

	// U линейное BC
	static char parname_NUBC[]		= "N_U_BC";
	param[NUBC].name 				= parname_NUBC;
	param[NUBC].type 				= PARAM_TYPE_ANALOG;
	param[NUBC].module 				= &module[MODULES_50_A4];
	param[NUBC].addrr 				= MOD380_ADDR_RMS + MOD380_CH_02;
	param[NUBC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[NUBC].coef 			= &coefs[N_U_BC_k];
	mas_calibr[NUBC].calibr 		= param_calibr_line_voltage;
	param[NUBC].calibr_obj			= &mas_calibr[NUBC];
	// Фильтр скользящим средним
	param[NUBC].filter_obj.filter_type 		= f_no_filter;// f_moving_average; mydebug_burn
	param[NUBC].filter_obj.filter_ptr.fma	= &N_U_BC_FILTER;
	err = param_init(&param[NUBC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NUBC], param[NUBC].name, 1);

	// U линейное AC
	static char parname_NUAC[]		= "N_U_AC";
	param[NUAC].name 				= parname_NUAC;
	param[NUAC].type 				= PARAM_TYPE_ANALOG;
	param[NUAC].module 				= &module[MODULES_50_A4];
	param[NUAC].addrr 				= MOD380_ADDR_RMS + MOD380_CH_03;
	param[NUAC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[NUAC].coef 			= &coefs[N_U_AC_k];
	mas_calibr[NUAC].calibr 		= param_calibr_line_voltage;
	param[NUAC].calibr_obj			= &mas_calibr[NUAC];
	// Фильтр скользящим средним
	param[NUAC].filter_obj.filter_type 		= f_no_filter;// f_moving_average; mydebug_burn
	param[NUAC].filter_obj.filter_ptr.fma	= &N_U_AC_FILTER;
	err = param_init(&param[NUAC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NUAC], param[NUAC].name, 1);

	// F U фазы A
	static char parname_NFUA[]		= "N_F_U_A";
	param[NFUA].name 				= parname_NFUA;
	param[NFUA].type 				= PARAM_TYPE_ANALOG;
	param[NFUA].module 				= &module[MODULES_50_A4];
	param[NFUA].addrr 				= MOD380_ADDR_FREQ + MOD380_CH_01;
	param[NFUA].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[NFUA].coef 			= &coefs[N_F_U_A_k];
	mas_calibr[NFUA].calibr 		= param_calibr_line_frequency_net;
	param[NFUA].calibr_obj			= &mas_calibr[NFUA];
	// Фильтр скользящим средним
	param[NFUA].filter_obj.filter_type 		= f_moving_average;
	param[NFUA].filter_obj.filter_ptr.fma	= &N_F_U_A_FILTER;
	err = param_init(&param[NFUA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NFUA], param[NFUA].name, 1);

	// F U фазы B
	static char parname_NFUB[]		= "N_F_U_B";
	param[NFUB].name 				= parname_NFUB;
	param[NFUB].type 				= PARAM_TYPE_ANALOG;
	param[NFUB].module 				= &module[MODULES_50_A4];
	param[NFUB].addrr 				= MOD380_ADDR_FREQ + MOD380_CH_02;
	param[NFUB].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[NFUB].coef 			= &coefs[N_F_U_B_k];
	mas_calibr[NFUB].calibr 		= param_calibr_line_frequency_net;
	param[NFUB].calibr_obj			= &mas_calibr[NFUB];
	// Фильтр скользящим средним
	param[NFUB].filter_obj.filter_type 		= f_moving_average;
	param[NFUB].filter_obj.filter_ptr.fma	= &N_F_U_B_FILTER;
	err = param_init(&param[NFUB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NFUB], param[NFUB].name, 1);

	// F U фазы C
	static char parname_NFUC[]		= "N_F_U_C";
	param[NFUC].name 				= parname_NFUC;
	param[NFUC].type 				= PARAM_TYPE_ANALOG;
	param[NFUC].module 				= &module[MODULES_50_A4];
	param[NFUC].addrr 				= MOD380_ADDR_FREQ + MOD380_CH_03;
	param[NFUC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[NFUC].coef 			= &coefs[N_F_U_C_k];
	mas_calibr[NFUC].calibr 		= param_calibr_line_frequency_net;
	param[NFUC].calibr_obj			= &mas_calibr[NFUC];
	// Фильтр скользящим средним
	param[NFUC].filter_obj.filter_type 		= f_moving_average;
	param[NFUC].filter_obj.filter_ptr.fma	= &N_F_U_C_FILTER;
	err = param_init(&param[NFUC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NFUC], param[NFUC].name, 1);

	// Угол U фазы A
	static char parname_NPHIUA[]	= "N_PHI_U_A";
	param[NPHIUA].name 				= parname_NPHIUA;
	param[NPHIUA].type 				= PARAM_TYPE_ANALOG;
	param[NPHIUA].module 			= &module[MODULES_50_A4];
	param[NPHIUA].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_01;
	param[NPHIUA].read 				= mod380_read_val_int;
	//Линейная аппроксимация
	param[NPHIUA].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[NPHIUA].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[NPHIUA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NPHIUA], param[NPHIUA].name, 3);

	// Угол U фазы B
	static char parname_NPHIUB[]	= "N_PHI_U_B";
	param[NPHIUB].name 				= parname_NPHIUB;
	param[NPHIUB].type 				= PARAM_TYPE_ANALOG;
	param[NPHIUB].module 			= &module[MODULES_50_A4];
	param[NPHIUB].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_02;
	param[NPHIUB].read 				= mod380_read_val_int;
	//Линейная аппроксимация
	param[NPHIUB].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[NPHIUB].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[NPHIUB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NPHIUB], param[NPHIUB].name, 3);

	// Угол U фазы C
	static char parname_NPHIUC[]	= "N_PHI_U_C";
	param[NPHIUC].name 				= parname_NPHIUC;
	param[NPHIUC].type 				= PARAM_TYPE_ANALOG;
	param[NPHIUC].module 			= &module[MODULES_50_A4];
	param[NPHIUC].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_03;
	param[NPHIUC].read 				= mod380_read_val_int;
	//Линейная аппроксимация
	param[NPHIUC].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[NPHIUC].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[NPHIUC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NPHIUC], param[NPHIUC].name, 3);

	// I фазы А
	static char parname_NIA[]		= "N_I_A";
	param[NIA].name 				= parname_NIA;
	param[NIA].type 				= PARAM_TYPE_ANALOG;
	param[NIA].module 				= &module[MODULES_50_A4];
	param[NIA].addrr 				= MOD380_ADDR_RMS + MOD380_CH_04;
	param[NIA].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[NIA].coef 			= &coefs[N_I_A_k];
	mas_calibr[NIA].calibr 			= param_calibr_line_1_positive;
	param[NIA].calibr_obj			= &mas_calibr[NIA];
	// Фильтр скользящим средним
	param[NIA].filter_obj.filter_type 		= f_no_filter;// f_moving_average; mydebug_burn
	param[NIA].filter_obj.filter_ptr.fma	= &N_I_A_FILTER;
	err = param_init(&param[NIA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NIA], param[NIA].name, 1);

	// I фазы B
	static char parname_NIB[]		= "N_I_B";
	param[NIB].name 				= parname_NIB;
	param[NIB].type 				= PARAM_TYPE_ANALOG;
	param[NIB].module 				= &module[MODULES_50_A4];
	param[NIB].addrr 				= MOD380_ADDR_RMS + MOD380_CH_05;
	param[NIB].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[NIB].coef 			= &coefs[N_I_B_k];
	mas_calibr[NIB].calibr 			= param_calibr_line_1_positive;
	param[NIB].calibr_obj			= &mas_calibr[NIB];
	// Фильтр скользящим средним
	param[NIB].filter_obj.filter_type 		= f_no_filter;// f_moving_average; mydebug_burn
	param[NIB].filter_obj.filter_ptr.fma	= &N_I_B_FILTER;
	err = param_init(&param[NIB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NIB], param[NIB].name, 1);

	// I фазы C
	static char parname_NIC[]		= "N_I_C";
	param[NIC].name 				= parname_NIC;
	param[NIC].type 				= PARAM_TYPE_ANALOG;
	param[NIC].module 				= &module[MODULES_50_A4];
	param[NIC].addrr 				= MOD380_ADDR_RMS + MOD380_CH_06;
	param[NIC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[NIC].coef 			= &coefs[N_I_C_k];
	mas_calibr[NIC].calibr 			= param_calibr_line_1_positive;
	param[NIC].calibr_obj			= &mas_calibr[NIC];
	// Фильтр скользящим средним
	param[NIC].filter_obj.filter_type 		= f_no_filter;// f_moving_average; mydebug_burn
	param[NIC].filter_obj.filter_ptr.fma	= &N_I_C_FILTER;
	err = param_init(&param[NIC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NIC], param[NIC].name, 1);

	// Угол I фазы A
	static char parname_NPHIIA[]	= "N_PHI_I_A";
	param[NPHIIA].name 				= parname_NPHIIA;
	param[NPHIIA].type 				= PARAM_TYPE_ANALOG;
	param[NPHIIA].module 			= &module[MODULES_50_A4];
	param[NPHIIA].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_04;
	param[NPHIIA].read 				= mod380_read_val_int;
	//Линейная аппроксимация
	param[NPHIIA].calibr_obj		= 0;
	// Фильтр скользящим средним
	param[NPHIIA].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[NPHIIA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NPHIIA], param[NPHIIA].name, 3);

	// Угол I фазы B
	static char parname_NPHIIB[]	= "N_PHI_I_B";
	param[NPHIIB].name 				= parname_NPHIIB;
	param[NPHIIB].type 				= PARAM_TYPE_ANALOG;
	param[NPHIIB].module 			= &module[MODULES_50_A4];
	param[NPHIIB].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_05;
	param[NPHIIB].read 				= mod380_read_val_int;
	//Линейная аппроксимация
	param[NPHIIB].calibr_obj		= 0;
	// Фильтр скользящим средним
	param[NPHIIB].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[NPHIIB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NPHIIB], param[NPHIIB].name, 3);

	// Угол I фазы C
	static char parname_NPHIIC[]	= "N_PHI_I_C";
	param[NPHIIC].name 				= parname_NPHIIC;
	param[NPHIIC].type 				= PARAM_TYPE_ANALOG;
	param[NPHIIC].module 			= &module[MODULES_50_A4];
	param[NPHIIC].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_06;
	param[NPHIIC].read 				= mod380_read_val_int;
	//Линейная аппроксимация
	param[NPHIIC].calibr_obj		= 0;
	// Фильтр скользящим средним
	param[NPHIIC].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[NPHIIC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NPHIIC], param[NPHIIC].name, 3);

    // Состояние сети
	static char parname_NSTATE[] = "N_STATE";
	param[NSTATE].name 	= parname_NSTATE;
	param[NSTATE].type 	= PARAM_TYPE_EXT_RENEW;
	err = param_init(&param[NSTATE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);

	
	// Активная мощность
	static char parname_NP[] = "N_P";
	param[NP].name 	= parname_NP;
	param[NP].type 	= PARAM_TYPE_SECOND;
	param[NP].read 	= calc_p_net1;
	err = param_init(&param[NP]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NP], param[NP].name, 1);//my_debug
		
	// Реактивная мощность
	static char parname_NQ[] = "N_Q";
	param[NQ].name 	= parname_NQ;
	param[NQ].type 	= PARAM_TYPE_SECOND;
	param[NQ].read 	= calc_q_net1;
	err = param_init(&param[NQ]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NQ], param[NQ].name, 1);//my_debug

	// Полная мощность
	static char parname_NS[] = "N_S";
	param[NS].name 	= parname_NS;
	param[NS].type 	= PARAM_TYPE_SECOND;
	param[NS].read 	= calc_s_net1;
	err = param_init(&param[NS]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NS], param[NS].name, 10);

	// Косинус угла
	static char parname_NCOSPHI[] = "N_COS_PHI";
	param[NCOSPHI].name 	= parname_NCOSPHI;
	param[NCOSPHI].type 	= PARAM_TYPE_SECOND;
	param[NCOSPHI].read 	= calc_cos_net1;
	err = param_init(&param[NCOSPHI]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NCOSPHI], param[NCOSPHI].name, 10);
	
	// Фазировка
	static char parname_NPH[] 	= "N_PH";
	param[NPH].name 			= parname_NPH;
	param[NPH].type 			= PARAM_TYPE_SECOND;	
	param[NPH].read 			= calc_incorrect_net1;
	err = param_init(&param[NPH]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NPH], param[NPH].name, 5);

	// Обрыв фазы
	static char parname_NPHPHASE[] = "N_PH_PHASE";
	param[NPHPHASE].name 		= parname_NPHPHASE;
	param[NPHPHASE].type 		= PARAM_TYPE_SECOND;
	param[NPHPHASE].read 		= calc_break_net1;	
	err = param_init(&param[NPHPHASE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[NPHPHASE], param[NPHPHASE].name, 1);

    // Сводный параметр "Аварии сети"
	static char parname_EVENTSNET[] 	= "EVENTS_NET";
	param[EVENTSNET].name 				= parname_EVENTSNET;
	param[EVENTSNET].type 				= PARAM_TYPE_SECOND;
	param[EVENTSNET].addrr  			= 0;
	param[EVENTSNET].read 				= make_events_net;
	err = param_init(&param[EVENTSNET]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[EVENTSNET], param[EVENTSNET].name, 5);

	// Донесение "Контактор ввода сети"
	static char parname_NCONT[] = "N_CONT";
	init_discrete(NCONT, MODULES_50_A8, DISCR_CH_01, parname_NCONT, 1);

	// U линейное AB2
	static char parname_NUAB2[]		= "N_U_AB2";
	param[NUAB2].name 				= parname_NUAB2;
	param[NUAB2].type 				= PARAM_TYPE_ANALOG;
	param[NUAB2].module 			= &module[MODULES_50_A6];
	param[NUAB2].addrr 				= MOD380_ADDR_RMS + MOD380_CH_04;
	param[NUAB2].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[NUAB2].coef 			= &coefs[N_U_AB2_k];
	mas_calibr[NUAB2].calibr 		= param_calibr_line_1_positive;
	param[NUAB2].calibr_obj			= &mas_calibr[NUAB2];
	// Фильтр скользящим средним
	param[NUAB2].filter_obj.filter_type 	= f_moving_average;
	param[NUAB2].filter_obj.filter_ptr.fma	= &N_U_AB2_FILTER;
	err = param_init(&param[NUAB2]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[NUAB2], param[NUAB2].name, 3);

	// F U фазы A2
	static char parname_NFUA2[]		= "N_F_U_A2";
	param[NFUA2].name 				= parname_NFUA2;
	param[NFUA2].type 				= PARAM_TYPE_ANALOG;
	param[NFUA2].module 			= &module[MODULES_50_A6];
	param[NFUA2].addrr 				= MOD380_ADDR_FREQ + MOD380_CH_04;
	param[NFUA2].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[NFUA2].coef 			= &coefs[N_F_U_A2_k];
	mas_calibr[NFUA2].calibr 		= param_calibr_line_1_positive;
	param[NFUA2].calibr_obj			= &mas_calibr[NFUA2];
	// Фильтр скользящим средним
	param[NFUA2].filter_obj.filter_type 		= f_moving_average;
	param[NFUA2].filter_obj.filter_ptr.fma	= &N_F_U_A2_FILTER;
	err = param_init(&param[NFUA2]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[NFUA2], param[NFUA2].name, 1);

	// Угол U фазы A2
	static char parname_NPHIUA2[]	= "N_PHI_U_A2";
	param[NPHIUA2].name 			= parname_NPHIUA2;
	param[NPHIUA2].type 			= PARAM_TYPE_ANALOG;
	param[NPHIUA2].module 			= &module[MODULES_50_A6];
	param[NPHIUA2].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_04;
	param[NPHIUA2].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	param[NPHIUA2].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[NPHIUA2].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[NPHIUA2]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[NPHIUA2], param[NPHIUA2].name, 1);

    //Состояния источника Сети 1
    static char parname_N1SOURCESTATE[] = "N1_SOURCE_STATE";
	param[N1SOURCESTATE].name 	= parname_N1SOURCESTATE;
	param[N1SOURCESTATE].type 	= PARAM_TYPE_SECOND;
	param[N1SOURCESTATE].read 	= calc_net1devstate;
	err = param_init(&param[N1SOURCESTATE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[N1SOURCESTATE], param[N1SOURCESTATE].name, 2);

}// End of init_params_net1

void init_params_net2()
{
	int8_t err = 0;

	// U линейное AB
	static char parname_N2UAB[]		= "N2_U_AB";
	param[N2UAB].name 				= parname_N2UAB;
	param[N2UAB].type 				= PARAM_TYPE_ANALOG;
	param[N2UAB].module 			= &module[MODULES_50_A5];
	param[N2UAB].addrr 				= MOD380_ADDR_RMS + MOD380_CH_01;
	param[N2UAB].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[N2UAB].coef 			= &coefs[N2_U_AB_k];
	mas_calibr[N2UAB].calibr 		= param_calibr_line_voltage;
	param[N2UAB].calibr_obj			= &mas_calibr[N2UAB];
	// Фильтр скользящим средним
	param[N2UAB].filter_obj.filter_type 		= f_moving_average;
	param[N2UAB].filter_obj.filter_ptr.fma	= &N2_U_AB_FILTER;
	err = param_init(&param[N2UAB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2UAB], param[N2UAB].name, 1);

	// U линейное BC
	static char parname_N2UBC[]		= "N2_U_BC";
	param[N2UBC].name 				= parname_N2UBC;
	param[N2UBC].type 				= PARAM_TYPE_ANALOG;
	param[N2UBC].module 			= &module[MODULES_50_A5];
	param[N2UBC].addrr 				= MOD380_ADDR_RMS + MOD380_CH_02;
	param[N2UBC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[N2UBC].coef 			= &coefs[N2_U_BC_k];
	mas_calibr[N2UBC].calibr 		= param_calibr_line_voltage;
	param[N2UBC].calibr_obj			= &mas_calibr[N2UBC];
	// Фильтр скользящим средним
	param[N2UBC].filter_obj.filter_type 		= f_moving_average;
	param[N2UBC].filter_obj.filter_ptr.fma	= &N2_U_BC_FILTER;
	err = param_init(&param[N2UBC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2UBC], param[N2UBC].name, 1);

	// U линейное AC
	static char parname_N2UAC[]		= "N2_U_AC";
	param[N2UAC].name 				= parname_N2UAC;
	param[N2UAC].type 				= PARAM_TYPE_ANALOG;
	param[N2UAC].module 			= &module[MODULES_50_A5];
	param[N2UAC].addrr 				= MOD380_ADDR_RMS + MOD380_CH_03;
	param[N2UAC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[N2UAC].coef 			= &coefs[N2_U_AC_k];
	mas_calibr[N2UAC].calibr 		= param_calibr_line_voltage;
	param[N2UAC].calibr_obj			= &mas_calibr[N2UAC];
	// Фильтр скользящим средним
	param[N2UAC].filter_obj.filter_type 		= f_moving_average;
	param[N2UAC].filter_obj.filter_ptr.fma	= &N2_U_AC_FILTER;
	err = param_init(&param[N2UAC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2UAC], param[N2UAC].name, 1);

	// F U фазы A
	static char parname_N2FUA[]		= "N2_F_U_A";
	param[N2FUA].name 				= parname_N2FUA;
	param[N2FUA].type 				= PARAM_TYPE_ANALOG;
	param[N2FUA].module 			= &module[MODULES_50_A5];
	param[N2FUA].addrr 				= MOD380_ADDR_FREQ + MOD380_CH_01;
	param[N2FUA].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[N2FUA].coef 			= &coefs[N2_F_U_A_k];
	mas_calibr[N2FUA].calibr 		= param_calibr_line_frequency_net2;
	param[N2FUA].calibr_obj			= &mas_calibr[N2FUA];
	// Фильтр скользящим средним
	param[N2FUA].filter_obj.filter_type 	= f_moving_average;
	param[N2FUA].filter_obj.filter_ptr.fma	= &N2_F_U_A_FILTER;
	err = param_init(&param[N2FUA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2FUA], param[N2FUA].name, 1);

	// F U фазы B
	static char parname_N2FUB[]		= "N2_F_U_B";
	param[N2FUB].name 				= parname_N2FUB;
	param[N2FUB].type 				= PARAM_TYPE_ANALOG;
	param[N2FUB].module 			= &module[MODULES_50_A5];
	param[N2FUB].addrr 				= MOD380_ADDR_FREQ + MOD380_CH_02;
	param[N2FUB].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[N2FUB].coef 			= &coefs[N2_F_U_B_k];
	mas_calibr[N2FUB].calibr 		= param_calibr_line_frequency_net2;
	param[N2FUB].calibr_obj			= &mas_calibr[N2FUB];
	// Фильтр скользящим средним
	param[N2FUB].filter_obj.filter_type 		= f_moving_average;
	param[N2FUB].filter_obj.filter_ptr.fma	= &N2_F_U_B_FILTER;
	err = param_init(&param[N2FUB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2FUB], param[N2FUB].name, 1);

	// F U фазы C
	static char parname_N2FUC[]		= "N2_F_U_C";
	param[N2FUC].name 				= parname_N2FUC;
	param[N2FUC].type 				= PARAM_TYPE_ANALOG;
	param[N2FUC].module 			= &module[MODULES_50_A5];
	param[N2FUC].addrr 				= MOD380_ADDR_FREQ + MOD380_CH_03;
	param[N2FUC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[N2FUC].coef 			= &coefs[N2_F_U_C_k];
	mas_calibr[N2FUC].calibr 		= param_calibr_line_frequency_net2;
	param[N2FUC].calibr_obj			= &mas_calibr[N2FUC];
	// Фильтр скользящим средним
	param[N2FUC].filter_obj.filter_type 		= f_moving_average;
	param[N2FUC].filter_obj.filter_ptr.fma	= &N2_F_U_C_FILTER;
	err = param_init(&param[N2FUC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2FUC], param[N2FUC].name, 1);

	// Угол U фазы A
	static char parname_N2PHIUA[]	= "N2_PHI_U_A";
	param[N2PHIUA].name 			= parname_N2PHIUA;
	param[N2PHIUA].type 			= PARAM_TYPE_ANALOG;
	param[N2PHIUA].module 			= &module[MODULES_50_A5];
	param[N2PHIUA].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_01;
	param[N2PHIUA].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	param[N2PHIUA].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[N2PHIUA].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[N2PHIUA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2PHIUA], param[N2PHIUA].name, 3);

	// Угол U фазы B
	static char parname_N2PHIUB[]	= "N2_PHI_U_B";
	param[N2PHIUB].name 			= parname_N2PHIUB;
	param[N2PHIUB].type 			= PARAM_TYPE_ANALOG;
	param[N2PHIUB].module 			= &module[MODULES_50_A5];
	param[N2PHIUB].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_02;
	param[N2PHIUB].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	param[N2PHIUB].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[N2PHIUB].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[N2PHIUB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2PHIUB], param[N2PHIUB].name, 3);

	// Угол U фазы C
	static char parname_N2PHIUC[]	= "N2_PHI_U_C";
	param[N2PHIUC].name 			= parname_N2PHIUC;
	param[N2PHIUC].type 			= PARAM_TYPE_ANALOG;
	param[N2PHIUC].module 			= &module[MODULES_50_A5];
	param[N2PHIUC].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_03;
	param[N2PHIUC].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	param[N2PHIUC].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[N2PHIUC].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[N2PHIUC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2PHIUC], param[N2PHIUC].name, 3);

	// I фазы А
	static char parname_N2IA[]		= "N2_I_A";
	param[N2IA].name 				= parname_N2IA;
	param[N2IA].type 				= PARAM_TYPE_ANALOG;
	param[N2IA].module 				= &module[MODULES_50_A5];
	param[N2IA].addrr 				= MOD380_ADDR_RMS + MOD380_CH_04;
	param[N2IA].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[N2IA].coef 			= &coefs[N2_I_A_k];
	mas_calibr[N2IA].calibr 		= param_calibr_line_1_positive;
	param[N2IA].calibr_obj			= &mas_calibr[N2IA];
	// Фильтр скользящим средним
	param[N2IA].filter_obj.filter_type 		= f_moving_average;
	param[N2IA].filter_obj.filter_ptr.fma	= &N2_I_A_FILTER;
	err = param_init(&param[N2IA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2IA], param[N2IA].name, 3);

	// I фазы B
	static char parname_N2IB[]		= "N2_I_B";
	param[N2IB].name 				= parname_N2IB;
	param[N2IB].type 				= PARAM_TYPE_ANALOG;
	param[N2IB].module 				= &module[MODULES_50_A5];
	param[N2IB].addrr 				= MOD380_ADDR_RMS + MOD380_CH_05;
	param[N2IB].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[N2IB].coef 			= &coefs[N2_I_B_k];
	mas_calibr[N2IB].calibr 		= param_calibr_line_1_positive;
	param[N2IB].calibr_obj			= &mas_calibr[N2IB];
	// Фильтр скользящим средним
	param[N2IB].filter_obj.filter_type 		= f_moving_average;
	param[N2IB].filter_obj.filter_ptr.fma	= &N2_I_B_FILTER;
	err = param_init(&param[N2IB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2IB], param[N2IB].name, 3);

	// I фазы C
	static char parname_N2IC[]		= "N2_I_C";
	param[N2IC].name 				= parname_N2IC;
	param[N2IC].type 				= PARAM_TYPE_ANALOG;
	param[N2IC].module 				= &module[MODULES_50_A5];
	param[N2IC].addrr 				= MOD380_ADDR_RMS + MOD380_CH_06;
	param[N2IC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[N2IC].coef 			= &coefs[N2_I_C_k];
	mas_calibr[N2IC].calibr 		= param_calibr_line_1_positive;
	param[N2IC].calibr_obj			= &mas_calibr[N2IC];
	// Фильтр скользящим средним
	param[N2IC].filter_obj.filter_type 		= f_moving_average;
	param[N2IC].filter_obj.filter_ptr.fma	= &N2_I_C_FILTER;
	err = param_init(&param[N2IC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2IC], param[N2IC].name, 3);

	// Угол I фазы A
	static char parname_N2PHIIA[]	= "N2_PHI_I_A";
	param[N2PHIIA].name 			= parname_N2PHIIA;
	param[N2PHIIA].type 			= PARAM_TYPE_ANALOG;
	param[N2PHIIA].module 			= &module[MODULES_50_A5];
	param[N2PHIIA].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_04;
	param[N2PHIIA].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	param[N2PHIIA].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[N2PHIIA].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[N2PHIIA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2PHIIA], param[N2PHIIA].name, 3);

	// Угол I фазы B
	static char parname_N2PHIIB[]	= "N2_PHI_I_B";
	param[N2PHIIB].name 			= parname_N2PHIIB;
	param[N2PHIIB].type 			= PARAM_TYPE_ANALOG;
	param[N2PHIIB].module 			= &module[MODULES_50_A5];
	param[N2PHIIB].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_05;
	param[N2PHIIB].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	param[N2PHIIB].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[N2PHIIB].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[N2PHIIB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2PHIIB], param[N2PHIIB].name, 3);

	// Угол I фазы C
	static char parname_N2PHIIC[]	= "N2_PHI_I_C";
	param[N2PHIIC].name 			= parname_N2PHIIC;
	param[N2PHIIC].type 			= PARAM_TYPE_ANALOG;
	param[N2PHIIC].module 			= &module[MODULES_50_A5];
	param[N2PHIIC].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_06;
	param[N2PHIIC].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	param[N2PHIIC].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[N2PHIIC].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[N2PHIIC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2PHIIC], param[N2PHIIC].name, 3);

    // Активная мощность Сети2. 
	static char parname_N2P[] = "N2_P";
	param[N2P].name 		= parname_N2P;
	param[N2P].type 		= PARAM_TYPE_SECOND;
	param[N2P].read 		= calc_p_net2;
	err = param_init(&param[N2P]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2P], param[N2P].name, 10);
		
	// Реактивная мощность Сети2. 
	static char parname_N2Q[] 	= "N2_Q";
	param[N2Q].name 			= parname_N2Q;
	param[N2Q].type 			= PARAM_TYPE_SECOND;
	param[N2Q].read 			= calc_q_net2;
	err = param_init(&param[N2Q]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2Q], param[N2Q].name, 10);

	// Полная мощность Сети2. 
	static char parname_N2S[] 	= "N2_S";
	param[N2S].name 			= parname_N2S;
	param[N2S].type 			= PARAM_TYPE_SECOND;
	param[N2S].read 			= calc_s_net2;
	err = param_init(&param[N2S]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2S], param[N2S].name, 10);

	// Косинус угла Сети2. 
	static char parname_N2COSPHI[] 	= "N2_COS_PHI";
	param[N2COSPHI].name 			= parname_N2COSPHI;
	param[N2COSPHI].type 			= PARAM_TYPE_SECOND;
	param[N2COSPHI].read 			= calc_cos_net2;
	err = param_init(&param[N2COSPHI]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2COSPHI], param[N2COSPHI].name, 10);
	
	// Фазировка Сети2
	static char parname_N2PH[] 		= "N2_PH";
	param[N2PH].name 				= parname_N2PH;
	param[N2PH].type 				= PARAM_TYPE_SECOND;	
	param[N2PH].read 				= calc_incorrect_net2;
	err = param_init(&param[N2PH]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2PH], param[N2PH].name, 5);

	// Обрыв фазы Сети2
	static char parname_N2PHPHASE[] = "N2_PH_PHASE";
	param[N2PHPHASE].name 			= parname_N2PHPHASE;
	param[N2PHPHASE].type 			= PARAM_TYPE_SECOND;
	param[N2PHPHASE].read 			= calc_break_net2;	
	err = param_init(&param[N2PHPHASE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[N2PHPHASE], param[N2PHPHASE].name, 1);

	// Состояние сети
	static char parname_N2STATE[] 	= "N2_STATE";
	param[N2STATE].name 			= parname_N2STATE;
	param[N2STATE].type 			= PARAM_TYPE_EXT_RENEW;
	err = param_init(&param[N2STATE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);

	// Норма cети
	static char parname_N2NORM[] = "N2_NORM";
	param[N2NORM].name 	= parname_N2NORM;
	param[N2NORM].type 	= PARAM_TYPE_SECOND;
	param[N2NORM].addrr = N2_STATE;
	param[N2NORM].read 	= calc_nnorm;
	err = param_init(&param[N2NORM]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[N2NORM], param[N2NORM].name, 2);

	// Донесение "Контактор ввода сети2"
	static char parname_N2CONT[] = "N2_CONT";
	init_discrete(N2CONT, MODULES_50_A9, DISCR_CH_01, parname_N2CONT, 1);

	// U линейное AB2
	static char parname_N2UAB2[]	= "N2_U_AB2";
	param[N2UAB2].name 				= parname_N2UAB2;
	param[N2UAB2].type 				= PARAM_TYPE_ANALOG;
	param[N2UAB2].module 			= &module[MODULES_50_A6];
	param[N2UAB2].addrr 			= MOD380_ADDR_RMS + MOD380_CH_07;
	param[N2UAB2].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[N2UAB2].coef 		= &coefs[N2_U_AB2_k];
	mas_calibr[N2UAB2].calibr 		= param_calibr_line_1_positive;
	param[N2UAB2].calibr_obj		= &mas_calibr[N2UAB2];
	// Фильтр скользящим средним
	param[N2UAB2].filter_obj.filter_type 	= f_moving_average;
	param[N2UAB2].filter_obj.filter_ptr.fma	= &N2_U_AB2_FILTER;
	err = param_init(&param[N2UAB2]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[N2UAB2], param[N2UAB2].name, 3);

	// F U фазы A2
	static char parname_N2FUA2[]	= "N2_F_U_A2";
	param[N2FUA2].name 				= parname_N2FUA2;
	param[N2FUA2].type 				= PARAM_TYPE_ANALOG;
	param[N2FUA2].module 			= &module[MODULES_50_A6];
	param[N2FUA2].addrr 			= MOD380_ADDR_FREQ + MOD380_CH_07;
	param[N2FUA2].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[N2FUA2].coef 		= &coefs[N2_F_U_A2_k];
	mas_calibr[N2FUA2].calibr 		= param_calibr_line_1_positive;
	param[N2FUA2].calibr_obj		= &mas_calibr[N2FUA2];
	// Фильтр скользящим средним
	param[N2FUA2].filter_obj.filter_type 	= f_moving_average;
	param[N2FUA2].filter_obj.filter_ptr.fma	= &N2_F_U_A2_FILTER;
	err = param_init(&param[N2FUA2]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[N2FUA2], param[N2FUA2].name, 3);

	// Угол U фазы A2
	static char parname_N2PHIUA2[]	= "N2_PHI_U_A2";
	param[N2PHIUA2].name 			= parname_N2PHIUA2;
	param[N2PHIUA2].type 			= PARAM_TYPE_ANALOG;
	param[N2PHIUA2].module 			= &module[MODULES_50_A6];
	param[N2PHIUA2].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_07;
	param[N2PHIUA2].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	mas_calibr[N2PHIUA2].coef 		= 0;
	// Фильтр скользящим средним
	param[N2PHIUA2].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[N2PHIUA2]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[N2PHIUA2], param[N2PHIUA2].name, 1);

	// Сводный параметр "Аварии сети"
	static char parname_EVENTSNET2[] 	= "EVENTS_NET2";
	param[EVENTSNET2].name 				= parname_EVENTSNET2;
	param[EVENTSNET2].type 				= PARAM_TYPE_SECOND;
	param[EVENTSNET2].addrr  			= 0;
	param[EVENTSNET2].read 				= make_events_net2;
	err = param_init(&param[EVENTSNET2]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[EVENTSNET2], param[EVENTSNET2].name, 5);

    // Состояния источника Сети 2
    static char parname_N2SOURCESTATE[] = "N2_SOURCE_STATE";
	param[N2SOURCESTATE].name 	= parname_N2SOURCESTATE;
	param[N2SOURCESTATE].type 	= PARAM_TYPE_SECOND;
	param[N2SOURCESTATE].read 	= calc_net2devstate;
	err = param_init(&param[N2SOURCESTATE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[N2SOURCESTATE], param[N2SOURCESTATE].name, 2);


}// End of init_params_net2

void init_params_ea()
{
	int8_t err = 0;

	// U линейное AB
	static char parname_EAUAB[]		= "EA_U_AB";
	param[EAUAB].name 				= parname_EAUAB;
	param[EAUAB].type 				= PARAM_TYPE_ANALOG;
	param[EAUAB].module 			= &module[MODULES_50_A4];
	param[EAUAB].addrr 				= MOD380_ADDR_RMS + MOD380_CH_07;
	param[EAUAB].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[EAUAB].coef 			= &coefs[EA_U_AB_k];
	mas_calibr[EAUAB].calibr 		= param_calibr_line_1_positive;
	param[EAUAB].calibr_obj			= &mas_calibr[EAUAB];
	// Фильтр скользящим средним
	param[EAUAB].filter_obj.filter_type 	=  f_no_filter;// f_moving_average; mydebug_burn
	param[EAUAB].filter_obj.filter_ptr.fma	= &EA_U_AB_FILTER;
	err = param_init(&param[EAUAB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAUAB], param[EAUAB].name, 1);

	// U линейное BC
	static char parname_EAUBC[]		= "EA_U_BC";
	param[EAUBC].name 				= parname_EAUBC;
	param[EAUBC].type 				= PARAM_TYPE_ANALOG;
	param[EAUBC].module 			= &module[MODULES_50_A4];
	param[EAUBC].addrr 				= MOD380_ADDR_RMS + MOD380_CH_08;
	param[EAUBC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[EAUBC].coef 			= &coefs[EA_U_BC_k];
	mas_calibr[EAUBC].calibr 		= param_calibr_line_1_positive;
	param[EAUBC].calibr_obj			= &mas_calibr[EAUBC];
	// Фильтр скользящим средним
	param[EAUBC].filter_obj.filter_type 	= f_no_filter;// f_moving_average; mydebug_burn
	param[EAUBC].filter_obj.filter_ptr.fma	= &EA_U_BC_FILTER;
	err = param_init(&param[EAUBC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAUBC], param[EAUBC].name, 1);

	// U линейное AC
	static char parname_EAUAC[]		= "EA_U_AC";
	param[EAUAC].name 				= parname_EAUAC;
	param[EAUAC].type 				= PARAM_TYPE_ANALOG;
	param[EAUAC].module 			= &module[MODULES_50_A4];
	param[EAUAC].addrr 				= MOD380_ADDR_RMS + MOD380_CH_09;
	param[EAUAC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[EAUAC].coef 			= &coefs[EA_U_AC_k];
	mas_calibr[EAUAC].calibr 		= param_calibr_line_1_positive;
	param[EAUAC].calibr_obj			= &mas_calibr[EAUAC];
	// Фильтр скользящим средним
	param[EAUAC].filter_obj.filter_type 	= f_no_filter;// f_moving_average; mydebug_burn
	param[EAUAC].filter_obj.filter_ptr.fma	= &EA_U_AC_FILTER;
	err = param_init(&param[EAUAC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAUAC], param[EAUAC].name, 1);

	// F U фазы A
	static char parname_EAFUA[]		= "EA_F_U_A";
	param[EAFUA].name 				= parname_EAFUA;
	param[EAFUA].type 				= PARAM_TYPE_ANALOG;
	param[EAFUA].module 			= &module[MODULES_50_A4];
	param[EAFUA].addrr 				= MOD380_ADDR_FREQ + MOD380_CH_07;
	param[EAFUA].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[EAFUA].coef 			= &coefs[EA_F_U_A_k];
	mas_calibr[EAFUA].calibr 		= param_calibr_line_1_positive;
	param[EAFUA].calibr_obj			= &mas_calibr[EAFUA];
	// Фильтр скользящим средним
	param[EAFUA].filter_obj.filter_type 	= f_no_filter;// f_moving_average; mydebug_burn
	param[EAFUA].filter_obj.filter_ptr.fma	= &EA_F_U_A_FILTER;
	err = param_init(&param[EAFUA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAFUA], param[EAFUA].name, 1);

	// F U фазы B
	static char parname_EAFUB[]		= "EA_F_U_B";
	param[EAFUB].name 				= parname_EAFUB;
	param[EAFUB].type 				= PARAM_TYPE_ANALOG;
	param[EAFUB].module 			= &module[MODULES_50_A4];
	param[EAFUB].addrr 				= MOD380_ADDR_FREQ + MOD380_CH_08;
	param[EAFUB].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[EAFUB].coef 			= &coefs[EA_F_U_B_k];
	mas_calibr[EAFUB].calibr 		= param_calibr_line_1_positive;
	param[EAFUB].calibr_obj			= &mas_calibr[EAFUB];
	// Фильтр скользящим средним
	param[EAFUB].filter_obj.filter_type 	= f_moving_average;
	param[EAFUB].filter_obj.filter_ptr.fma	= &EA_F_U_B_FILTER;
	err = param_init(&param[EAFUB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAFUB], param[EAFUB].name, 1);

	// F U фазы C
	static char parname_EAFUC[]		= "EA_F_U_C";
	param[EAFUC].name 				= parname_EAFUC;
	param[EAFUC].type 				= PARAM_TYPE_ANALOG;
	param[EAFUC].module 			= &module[MODULES_50_A4];
	param[EAFUC].addrr 				= MOD380_ADDR_FREQ + MOD380_CH_09;
	param[EAFUC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[EAFUC].coef 			= &coefs[EA_F_U_C_k];
	mas_calibr[EAFUC].calibr 		= param_calibr_line_1_positive;
	param[EAFUC].calibr_obj			= &mas_calibr[EAFUC];
	// Фильтр скользящим средним
	param[EAFUC].filter_obj.filter_type 	= f_moving_average;
	param[EAFUC].filter_obj.filter_ptr.fma	= &EA_F_U_C_FILTER;
	err = param_init(&param[EAFUC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAFUC], param[EAFUC].name, 1);

	// Угол U фазы A
	static char parname_EAPHIUA[]	= "EA_PHI_U_A";
	param[EAPHIUA].name 			= parname_EAPHIUA;
	param[EAPHIUA].type 			= PARAM_TYPE_ANALOG;
	param[EAPHIUA].module 			= &module[MODULES_50_A4];
	param[EAPHIUA].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_07;
	param[EAPHIUA].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	param[EAPHIUA].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[EAPHIUA].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[EAPHIUA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAPHIUA], param[EAPHIUA].name, 3);

	// Угол U фазы B
	static char parname_EAPHIUB[]	= "EA_PHI_U_B";
	param[EAPHIUB].name 			= parname_EAPHIUB;
	param[EAPHIUB].type 			= PARAM_TYPE_ANALOG;
	param[EAPHIUB].module 			= &module[MODULES_50_A4];
	param[EAPHIUB].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_08;
	param[EAPHIUB].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	param[EAPHIUB].calibr_obj		= 0; 
    // Фильтр скользящим средним
	param[EAPHIUB].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[EAPHIUB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAPHIUB], param[EAPHIUB].name, 3);

	// Угол U фазы C
	static char parname_EAPHIUC[]	= "EA_PHI_U_C";
	param[EAPHIUC].name 			= parname_EAPHIUC;
	param[EAPHIUC].type 			= PARAM_TYPE_ANALOG;
	param[EAPHIUC].module 			= &module[MODULES_50_A4];
	param[EAPHIUC].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_09;
	param[EAPHIUC].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	param[EAPHIUC].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[EAPHIUC].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[EAPHIUC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAPHIUC], param[EAPHIUC].name, 3);

	// I фазы А
	static char parname_EAIA[]		= "EA_I_A";
	param[EAIA].name 				= parname_EAIA;
	param[EAIA].type 				= PARAM_TYPE_ANALOG;
	param[EAIA].module 				= &module[MODULES_50_A4];
	param[EAIA].addrr 				= MOD380_ADDR_RMS + MOD380_CH_10;
	param[EAIA].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[EAIA].coef 			= &coefs[EA_I_A_k];
	mas_calibr[EAIA].calibr 		= param_calibr_line_1_positive;
	param[EAIA].calibr_obj			= &mas_calibr[EAIA];
	// Фильтр скользящим средним
	param[EAIA].filter_obj.filter_type 	= f_no_filter;// f_moving_average; mydebug_burn
	param[EAIA].filter_obj.filter_ptr.fma	= &EA_I_A_FILTER;
	err = param_init(&param[EAIA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAIA], param[EAIA].name, 1);

	// I фазы B
	static char parname_EAIB[]		= "EA_I_B";
	param[EAIB].name 				= parname_EAIB;
	param[EAIB].type 				= PARAM_TYPE_ANALOG;
	param[EAIB].module 				= &module[MODULES_50_A4];
	param[EAIB].addrr 				= MOD380_ADDR_RMS + MOD380_CH_11;
	param[EAIB].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[EAIB].coef 			= &coefs[EA_I_B_k];
	mas_calibr[EAIB].calibr 		= param_calibr_line_1_positive;
	param[EAIB].calibr_obj			= &mas_calibr[EAIB];
	// Фильтр скользящим средним
	param[EAIB].filter_obj.filter_type 	= f_no_filter;// f_moving_average; mydebug_burn
	param[EAIB].filter_obj.filter_ptr.fma	= &EA_I_B_FILTER;
	err = param_init(&param[EAIB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAIB], param[EAIB].name, 1); 

	// I фазы C
	static char parname_EAIC[]		= "EA_I_C";
	param[EAIC].name 				= parname_EAIC;
	param[EAIC].type 				= PARAM_TYPE_ANALOG;
	param[EAIC].module 				= &module[MODULES_50_A4];
	param[EAIC].addrr 				= MOD380_ADDR_RMS + MOD380_CH_12;
	param[EAIC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[EAIC].coef 			= &coefs[EA_I_C_k];
	mas_calibr[EAIC].calibr 		= param_calibr_line_1_positive;
	param[EAIC].calibr_obj			= &mas_calibr[EAIC];
	// Фильтр скользящим средним
	param[EAIC].filter_obj.filter_type 	= f_no_filter;// f_moving_average; mydebug_burn
	param[EAIC].filter_obj.filter_ptr.fma	= &EA_I_C_FILTER;
	err = param_init(&param[EAIC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAIC], param[EAIC].name, 1);

	// Угол I фазы А
	static char parname_EAPHIIA[]	= "EA_PHI_I_A";
	param[EAPHIIA].name 			= parname_EAPHIIA;
	param[EAPHIIA].type 			= PARAM_TYPE_ANALOG;
	param[EAPHIIA].module 			= &module[MODULES_50_A4];
	param[EAPHIIA].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_10;
	param[EAPHIIA].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	param[EAPHIIA].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[EAPHIIA].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[EAPHIIA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAPHIIA], param[EAPHIIA].name, 3);

	// Угол I фазы B
	static char parname_EAPHIIB[]	= "EA_PHI_I_B";
	param[EAPHIIB].name 			= parname_EAPHIIB;
	param[EAPHIIB].type 			= PARAM_TYPE_ANALOG;
	param[EAPHIIB].module 			= &module[MODULES_50_A4];
	param[EAPHIIB].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_11;
	param[EAPHIIB].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	param[EAPHIIB].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[EAPHIIB].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[EAPHIIB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAPHIIB], param[EAPHIIB].name, 3);

	// Угол I фазы C
	static char parname_EAPHIIC[]	= "EA_PHI_I_C";
	param[EAPHIIC].name 			= parname_EAPHIIC;
	param[EAPHIIC].type 			= PARAM_TYPE_ANALOG;
	param[EAPHIIC].module 			= &module[MODULES_50_A4];
	param[EAPHIIC].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_12;
	param[EAPHIIC].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	param[EAPHIIC].calibr_obj		= 0; 
	// Фильтр скользящим средним
	param[EAPHIIC].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[EAPHIIC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAPHIIC], param[EAPHIIC].name, 3);

  // Активная мощность ЭА. 
	static char parname_EAP[] = "EA_P";
	param[EAP].name 	= parname_EAP;
	param[EAP].type 	= PARAM_TYPE_SECOND;
	param[EAP].read 	= calc_p_ea;
	err = param_init(&param[EAP]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAP], param[EAP].name, 1);//my_debug
				
	// Реактивная мощность ЭА. 
	static char parname_EAQ[] = "EA_Q";
	param[EAQ].name 	= parname_EAQ;
	param[EAQ].type 	= PARAM_TYPE_SECOND;
	param[EAQ].read 	= calc_q_ea;
	err = param_init(&param[EAQ]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAQ], param[EAQ].name, 1); //my_debug

	// Полная мощность ЭА. 
	static char parname_EAS[] = "EA_S";
	param[EAS].name 	= parname_EAS;
	param[EAS].type 	= PARAM_TYPE_SECOND;
	param[EAS].read 	= calc_s_ea;
	err = param_init(&param[EAS]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EAS], param[EAS].name, 10);

	// Косинус угла ЭА. 
	static char parname_EACOSPHI[]	= "EA_COS_PHI";
	param[EACOSPHI].name 			= parname_EACOSPHI;
	param[EACOSPHI].type 			= PARAM_TYPE_SECOND;
	param[EACOSPHI].read 			= calc_cos_ea;
	err = param_init(&param[EACOSPHI]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A4, &param[EACOSPHI], param[EACOSPHI].name, 10);

    /* Состояние ЭА. 
	** Krivenko S.A. Внимание: Этот параметр необходимо знать всем блокам управления.
	На BU_50 параметр настоящий и вычисляется алгоритмом ЭА*/
	static char parname_EASTATE[]	= "EA_STATE";
	param[EASTATE].name 			= parname_EASTATE;
	param[EASTATE].type 			= PARAM_TYPE_EXT_RENEW;
	err = param_init(&param[EASTATE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);

// Норма
//	EA_NORM,

	// t охлаждающей жидкости
	static char parname_EAtCOOL[] 	= "EA_t_COOL";
	param[EAtCOOL].name 			= parname_EAtCOOL;
	param[EAtCOOL].type 			= PARAM_TYPE_ANALOG;
	param[EAtCOOL].module 			= &module[MODULES_50_A3];
	param[EAtCOOL].addrr 			= MOD420_ADDR_ADC + MOD420_CH_08;
	param[EAtCOOL].read 			= mod420_read;
	//Линейная аппроксимация
	mas_calibr[EAtCOOL].coef 		= &coefs[EA_t_COOL_k];
	mas_calibr[EAtCOOL].calibr 		= param_calibr_line_1;
	param[EAtCOOL].calibr_obj		= &mas_calibr[EAtCOOL];
	// Фильтр скользящим средним
	param[EAtCOOL].filter_obj.filter_type = f_moving_average;
	param[EAtCOOL].filter_obj.filter_ptr.fma	= &EA_t_COOL_FILTER;
	err = param_init(&param[EAtCOOL]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[EAtCOOL], param[EAtCOOL].name, 10);

	// P масла
	static char parname_EAPOIL[] 	= "EA_P_OIL";
	param[EAPOIL].name 				= parname_EAPOIL;
	param[EAPOIL].type 				= PARAM_TYPE_ANALOG;
	param[EAPOIL].module 			= &module[MODULES_50_A3];
	param[EAPOIL].addrr 			= MOD420_ADDR_ADC + MOD420_CH_05;
	param[EAPOIL].read 				= mod420_read;
	//Линейная аппроксимация
	mas_calibr[EAPOIL].coef 		= &coefs[EA_P_OIL_k];
	mas_calibr[EAPOIL].calibr 		= param_calibr_line_1_positive;
	param[EAPOIL].calibr_obj		= &mas_calibr[EAPOIL];
	// Фильтр скользящим средним
	param[EAPOIL].filter_obj.filter_type = f_moving_average;
	param[EAPOIL].filter_obj.filter_ptr.fma	= &EA_P_OIL_FILTER;
	err = param_init(&param[EAPOIL]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[EAPOIL], param[EAPOIL].name, 3);

    // Пониженное давление масла
	static char parname_EAPOILNEW[] = "EA_P_OIL_NEW";
	param[EAPOILNEW].name 	= parname_EAPOILNEW;
	param[EAPOILNEW].type 	= PARAM_TYPE_SECOND;
	param[EAPOILNEW].addrr 	= EAPOIL;
	param[EAPOILNEW].read 	= calc_ea_p_oil_new;
	err = param_init(&param[EAPOILNEW]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[EAPOILNEW], param[EAPOILNEW].name, 10);

	// t масла
	static char parname_EAtOIL[] 	= "EA_t_OIL";
	param[EAtOIL].name 				= parname_EAtOIL;
	param[EAtOIL].type 				= PARAM_TYPE_ANALOG;
	param[EAtOIL].module 			= &module[MODULES_50_A3];
	param[EAtOIL].addrr 			= MOD420_ADDR_ADC + MOD420_CH_07;
	param[EAtOIL].read 				= mod420_read;
	//Линейная аппроксимация
	mas_calibr[EAtOIL].coef 		= &coefs[EA_t_OIL_k];
	mas_calibr[EAtOIL].calibr 		= param_calibr_line_1;
	param[EAtOIL].calibr_obj		= &mas_calibr[EAtOIL];
	// Фильтр скользящим средним
	param[EAtOIL].filter_obj.filter_type = f_moving_average;
	param[EAtOIL].filter_obj.filter_ptr.fma	= &EA_t_OIL_FILTER;
	err = param_init(&param[EAtOIL]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[EAtOIL], param[EAtOIL].name, 10);
    
    //Инициализруется в потоке diesel
    //Топливный клапан
	static char parname_FUEL[] = "FUEL";
	param[FUEL].name 	= parname_FUEL;
	param[FUEL].type 	= PARAM_TYPE_EXT_RENEW;
	err = param_init(&param[FUEL]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);

    //Аварии ЭА. Сводный параметр 
	static char parname_EVENTSEA[] = "EVENTS_EA";
	param[EVENTSEA].name 	= parname_EVENTSEA;
	param[EVENTSEA].type 	= PARAM_TYPE_SECOND;
	param[EVENTSEA].addrr 	= 0;
	param[EVENTSEA].read 	= make_alarms_ea;
	err = param_init(&param[EVENTSEA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[EVENTSEA], param[EVENTSEA].name, 5);

    //АСУ для вывода на ПУ
	static char parname_ASUEACALC[] = "ASU_EA_CALC";
	param[ASUEACALC].name 	= parname_ASUEACALC;
	param[ASUEACALC].type 	= PARAM_TYPE_EXT_RENEW;
	param[ASUEACALC].addrr 	= 0;
	err = param_init(&param[ASUEACALC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	param[ASUEACALC].value.val_int 	= 0;

    // Наработка ЭА
	static char parname_EAMOTOHOURS[] = "EA_MOTOHOURS";
	param[EAMOTOHOURS].name 	= parname_EAMOTOHOURS;
	param[EAMOTOHOURS].type 	= PARAM_TYPE_SECOND;
	param[EAMOTOHOURS].addrr 	= 0;
	param[EAMOTOHOURS].read 	= calc_motohours;
	err = param_init(&param[EAMOTOHOURS]);
	periodic_add_item(&params_periodic, &param[EAMOTOHOURS], param[EAMOTOHOURS].name,	100);

  // Наработка с перегрузом 10 %
	static char parname_EAMOTOHOURS10[] = "EA_MOTOHOURS10";
	param[EAMOTOHOURS10].name 	= parname_EAMOTOHOURS10;
	param[EAMOTOHOURS10].type 	= PARAM_TYPE_SECOND;
	param[EAMOTOHOURS10].addrr 	= 0;
	param[EAMOTOHOURS10].read 	= calc_motohours10;
	err = param_init(&param[EAMOTOHOURS10]);
	periodic_add_item(&params_periodic, &param[EAMOTOHOURS10], param[EAMOTOHOURS10].name,	100);
		
    // Наработка с ЭА в часах
	static char parname_EAHOURS[] = "EA_HOURS";
	param[EAHOURS].name 	= parname_EAHOURS;
	param[EAHOURS].type 	= PARAM_TYPE_SECOND;
	param[EAHOURS].addrr 	= EAMOTOHOURS;
	param[EAHOURS].read 	= calc_hours;
	err = param_init(&param[EAHOURS]);
	periodic_add_item(&params_periodic, &param[EAHOURS], param[EAHOURS].name,	100);

	// Наработка с перегрузом 10 % в часах
	static char parname_EAHOURS10[] = "EA_HOURS10";
	param[EAHOURS10].name 	= parname_EAHOURS10;
	param[EAHOURS10].type 	= PARAM_TYPE_SECOND;
	param[EAHOURS10].addrr 	= EAMOTOHOURS10;
	param[EAHOURS10].read 	= calc_hours;
	err = param_init(&param[EAHOURS10]);
	periodic_add_item(&params_periodic, &param[EAHOURS10], param[EAHOURS10].name,	100);

    // Время до ТО
	static char parname_EAMOTOHOURSLEFT[] = "EA_MOTOHOURS_LEFT";
	param[EAMOTOHOURSLEFT].name 	= parname_EAMOTOHOURSLEFT;
	param[EAMOTOHOURSLEFT].type 	= PARAM_TYPE_SECOND;
	param[EAMOTOHOURSLEFT].addrr 	= 0;
	param[EAMOTOHOURSLEFT].read 	= calc_motohours_left;
	err = param_init(&param[EAMOTOHOURSLEFT]);
	periodic_add_item(&params_periodic, &param[EAMOTOHOURSLEFT], param[EAMOTOHOURSLEFT].name,	100);

    // Обрыв датчика давления масла 
	static char parname_EAPOILCALC[] = "EA_P_OIL_CALC";
	param[EAPOILCALC].name 	= parname_EAPOILCALC;
	param[EAPOILCALC].type 	= PARAM_TYPE_SECOND;
	param[EAPOILCALC].addrr 	= EAPOIL;
	param[EAPOILCALC].read 	= calc_ea_p_oil;
	err = param_init(&param[EAPOILCALC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[EAPOILCALC], param[EAPOILCALC].name, 10);

	// Донесение "Контактор ЭА"
	static char parname_EACONT[] = "EA_CONT";
	init_discrete(EACONT, MODULES_50_A8, DISCR_CH_02, parname_EACONT, 1);

	// Донесение "Наличие ОЖ"
	static char parname_EACOOLNORM[] = "EA_COOL_NORM";
	init_discrete(EACOOLNORM, MODULES_50_A7, DISCR_CH_02, parname_EACOOLNORM, 5);

	// Донесение "Воздушный фильтр"
	static char parname_EAFILTERNORM[] = "EA_FILTER_NORM";
	init_discrete(EAFILTERNORM, MODULES_50_A7, DISCR_CH_01, parname_EAFILTERNORM, 5);

	// Донесение "МКИ включен"
	static char parname_BMKION[] = "B_MKI_ON";
	init_discrete(BMKION, MODULES_50_A8, DISCR_CH_06, parname_BMKION, 5);

	// Донесение "Не норма изоляции МКИ"
	static char parname_BMKIAI[] = "B_MKI_AI";
	init_discrete(BMKIAI, MODULES_50_A8, DISCR_CH_18, parname_BMKIAI, 5);

	// U линейное AB2
	static char parname_EAUAB2[]	= "EA_U_AB2";
	param[EAUAB2].name 				= parname_EAUAB2;
	param[EAUAB2].type 				= PARAM_TYPE_ANALOG;
	param[EAUAB2].module 			= &module[MODULES_50_A6];
	param[EAUAB2].addrr 			= MOD380_ADDR_RMS + MOD380_CH_05;
	param[EAUAB2].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[EAUAB2].coef 		= &coefs[EA_U_AB2_k];
	mas_calibr[EAUAB2].calibr 		= param_calibr_line_1_positive;
	param[EAUAB2].calibr_obj		= &mas_calibr[EAUAB2];
	// Фильтр скользящим средним
	param[EAUAB2].filter_obj.filter_type 	= f_moving_average;
	param[EAUAB2].filter_obj.filter_ptr.fma	= &EA_U_AB2_FILTER;
	err = param_init(&param[EAUAB2]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[EAUAB2], param[EAUAB2].name, 3);

	// F U фазы A2
	static char parname_EAFUA2[]	= "EA_F_U_A2";
	param[EAFUA2].name 				= parname_EAFUA2;
	param[EAFUA2].type 				= PARAM_TYPE_ANALOG;
	param[EAFUA2].module 			= &module[MODULES_50_A6];
	param[EAFUA2].addrr 			= MOD380_ADDR_FREQ + MOD380_CH_05;
	param[EAFUA2].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[EAFUA2].coef 		= &coefs[EA_F_U_A2_k];
	mas_calibr[EAFUA2].calibr 		= param_calibr_line_1_positive;
	param[EAFUA2].calibr_obj		= &mas_calibr[EAFUA2];
	// Фильтр скользящим средним
	param[EAFUA2].filter_obj.filter_type 	= f_no_filter;// f_moving_average; mydebug_burn
	param[EAFUA2].filter_obj.filter_ptr.fma	= &EA_F_U_A2_FILTER;
	err = param_init(&param[EAFUA2]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[EAFUA2], param[EAFUA2].name, 1);

	// Угол U фазы A2
	static char parname_EAPHIUA2[]	= "EA_PHI_U_A2";
	param[EAPHIUA2].name 			= parname_EAPHIUA2;
	param[EAPHIUA2].type 			= PARAM_TYPE_ANALOG;
	param[EAPHIUA2].module 			= &module[MODULES_50_A6];
	param[EAPHIUA2].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_05;
	param[EAPHIUA2].read 			= mod380_read_val_int;
	//Линейная аппроксимация
	mas_calibr[EAPHIUA2].coef 		= 0;
	// Фильтр скользящим средним
	param[EAPHIUA2].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[EAPHIUA2]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[EAPHIUA2], param[EAPHIUA2].name, 1);

	// Донесение "Зарядный генератор"
	static char parname_CHARGEGEN[] = "CHARGE_GEN";
	init_discrete(CHARGEGEN, MODULES_50_A7, DISCR_CH_08, parname_CHARGEGEN, 5);

	// Донесение "Норма температуры генератора"
	static char parname_TGENNORM[] = "T_GEN_NORM";
	init_discrete(TGENNORM, MODULES_50_A7, DISCR_CH_04, parname_TGENNORM, 5);

	// Донесение "Норма температуры заднего подшипника"
	static char parname_TBEARINGNORM[] = "T_BEARING_NORM";
	init_discrete(TBEARINGNORM, MODULES_50_A7, DISCR_CH_05, parname_TBEARINGNORM, 5);

	// Донесение "Питание стартера от АБ СТ"
	static char parname_STARTERFROMABSTK1[] = "STARTER_FROM_AB_ST_K1";
	init_discrete(STARTERFROMABSTK1, MODULES_50_A7, DISCR_CH_06, parname_STARTERFROMABSTK1, 5);

	// Донесение "Питание стартера от АБ ХД"
	static char parname_STARTERFROMABSHASSISK2[] = "STARTER_FROM_AB_SHASSIS_K2";
	init_discrete(STARTERFROMABSHASSISK2, MODULES_50_A7, DISCR_CH_07, parname_STARTERFROMABSHASSISK2, 5);

//	// U корректора
//	U_CORR_EA,

    // Состояния источника ЭА
    static char parname_ELDEVSTATE[] = "EL_DEV_STATE";
	param[ELDEVSTATE].name 	= parname_ELDEVSTATE;
	param[ELDEVSTATE].type 	= PARAM_TYPE_SECOND;
	param[ELDEVSTATE].read 	= calc_eadevstate;
	err = param_init(&param[ELDEVSTATE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[ELDEVSTATE], param[ELDEVSTATE].name, 2);


}// End of init_params_ea

void init_params_en()
{
	int8_t err = 0;

	// I фазы A
	static char parname_ENIA[]		= "EN_I_A";
	param[ENIA].name 				= parname_ENIA;
	param[ENIA].type 				= PARAM_TYPE_ANALOG;
	param[ENIA].module 				= &module[MODULES_50_A5];
	param[ENIA].addrr 				= MOD380_ADDR_RMS + MOD380_CH_07;
	param[ENIA].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[ENIA].coef 			= &coefs[EN_I_A_k];
	mas_calibr[ENIA].calibr 		= param_calibr_line_1_positive;
	param[ENIA].calibr_obj			= &mas_calibr[ENIA];
	// Фильтр скользящим средним
	param[ENIA].filter_obj.filter_type 		= f_moving_average;
	param[ENIA].filter_obj.filter_ptr.fma	= &EN_I_A_FILTER;
	err = param_init(&param[ENIA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[ENIA], param[ENIA].name, 10);

	// I фазы B
	static char parname_ENIB[]		= "EN_I_B";
	param[ENIB].name 				= parname_ENIB;
	param[ENIB].type 				= PARAM_TYPE_ANALOG;
	param[ENIB].module 				= &module[MODULES_50_A5];
	param[ENIB].addrr 				= MOD380_ADDR_RMS + MOD380_CH_08;
	param[ENIB].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[ENIB].coef 			= &coefs[EN_I_B_k];
	mas_calibr[ENIB].calibr 		= param_calibr_line_1_positive;
	param[ENIB].calibr_obj			= &mas_calibr[ENIB];
	// Фильтр скользящим средним
	param[ENIB].filter_obj.filter_type 		= f_moving_average;
	param[ENIB].filter_obj.filter_ptr.fma	= &EN_I_B_FILTER;
	err = param_init(&param[ENIB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[ENIB], param[ENIB].name, 10);

	// I фазы C
	static char parname_ENIC[]		= "EN_I_C";
	param[ENIC].name 				= parname_ENIC;
	param[ENIC].type 				= PARAM_TYPE_ANALOG;
	param[ENIC].module 				= &module[MODULES_50_A5];
	param[ENIC].addrr 				= MOD380_ADDR_RMS + MOD380_CH_09;
	param[ENIC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[ENIC].coef 			= &coefs[EN_I_C_k];
	mas_calibr[ENIC].calibr 		= param_calibr_line_1_positive;
	param[ENIC].calibr_obj			= &mas_calibr[ENIC];
	// Фильтр скользящим средним
	param[ENIC].filter_obj.filter_type 		= f_moving_average;
	param[ENIC].filter_obj.filter_ptr.fma	= &EN_I_C_FILTER;
	err = param_init(&param[ENIC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[ENIC], param[ENIC].name, 10);

    static char parname_ENSTATE[] = "EN_STATE";
	param[ENSTATE].name 	= parname_ENSTATE;
	param[ENSTATE].type 	= PARAM_TYPE_EXT_RENEW;
	err = param_init(&param[ENSTATE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);

    static char parname_ENOILSTATE[] = "EN_OIL_STATE";
	param[ENOILSTATE].name 	= parname_ENOILSTATE;
	param[ENOILSTATE].type 	= PARAM_TYPE_EXT_RENEW;
	err = param_init(&param[ENOILSTATE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	
    // Донесение "Автомат ЭН"
	static char parname_ENAUT[] = "EN_AUT";
	init_discrete(ENAUT, MODULES_50_A9, DISCR_CH_11, parname_ENAUT, 5);

	// Донесение "Контактор ЭН"
	static char parname_ENCONT[] = "EN_CONT";
	init_discrete(ENCONT, MODULES_50_A9, DISCR_CH_02, parname_ENCONT, 1);

	// Донесение "Контактор ЭН масла"
	static char parname_ENOILCONT[] = "EN_OIL_CONT";
	init_discrete(ENOILCONT, MODULES_50_A9, DISCR_CH_24, parname_ENOILCONT, 1);
	
    // Донесение "Автомат ЭН отключен"
	static char parname_ENAUTOP[] = "EN_AUT_OP";
	init_discrete(ENAUTOP, MODULES_50_A9, DISCR_CH_10, parname_ENAUTOP, 5);

	// Донесение "Защита от перегрева ОЖ"
	static char parname_ENPROTECTION[] = "EN_PROTECTION";
	init_discrete(ENPROTECTION, MODULES_50_A9, DISCR_CH_09, parname_ENPROTECTION, 5);

}// End of init_params_en

//****************************************************************************************************
/** @details make_fcstarting1 - индикация режима запуска ПЧ100 1. Пока ПЧ100 запускается и проходит через режимы:
	fc_ad_starting,
	fc_ad_starting_source,
	fc_ad_starting_star_on,
	fc_ad_starting_star_rise,
	fc_ad_starting_star_wait,
	fc_ad_starting_star_off,
	fc_ad_starting_tria_on,
	fc_ad_starting_tria_wait параметр FC1_STARTING = 1, в другом случае параметр равен 0.
	Режимы взяты из файла fc_ad.h
	Параметр FC1_STARTING необходим чтобы отключать лимиты по току на генераторе, сети1, сети2.
	@return 0 - in any case.
*/
static int8_t make_fcstarting1(void* val)
{
	TParam *loc_prm = (TParam*)val;
	
	fc_ad_state_t loc_state = param[FC1AESTATE].value.val_int;
	
	if((loc_state >= fc_ad_starting) && (loc_state <= fc_ad_starting_tria_wait))
	{
		if (!loc_prm->value.val_int) debug_printf("%s %d: FC1_STARTING = 1 \n\r", __FILE__, __LINE__);
		loc_prm->value.val_int = 1;
	}
	else
	{
		if (loc_prm->value.val_int) debug_printf("%s %d: FC1_STARTING = 0 \n\r", __FILE__, __LINE__);
		loc_prm->value.val_int = 0;
	}
	return 0;
}
//****************************************************************************************************
/** @details make_fcstarting2 - индикация режима запуска ПЧ100 2. Пока ПЧ100 запускается и проходит через режимы:
	fc_ad_starting,
	fc_ad_starting_source,
	fc_ad_starting_star_on,
	fc_ad_starting_star_rise,
	fc_ad_starting_star_wait,
	fc_ad_starting_star_off,
	fc_ad_starting_tria_on,
	fc_ad_starting_tria_wait параметр FC1_STARTING = 1, в другом случае параметр равен 0.
	Режимы взяты из файла fc_ad.h
	Параметр FC1_STARTING необходим чтобы отключать лимиты по току на генераторе, сети1, сети2.
	@return 0 - in any case.
*/
static int8_t make_fcstarting2(void* val)
{
	TParam *loc_prm = (TParam*)val;
	
	fc_ad_state_t loc_state = param[FC2AESTATE].value.val_int;
	
	if((loc_state >= fc_ad_starting) && (loc_state <= fc_ad_starting_tria_wait)) loc_prm->value.val_int = 1;
	else loc_prm->value.val_int = 0;
	
	return 0;
}
//****************************************************************************************************
static int8_t make_fconoff1(void* val)
{
	TParam *loc_prm = (TParam*)val;
	fc_ad_state_t loc_state = param[FC1AESTATE].value.val_int;
	
	if((loc_state == fc_ad_off) || (loc_state == fc_ad_on) || (loc_state == fc_ad_error)) loc_prm->value.val_int = 1;
	else loc_prm->value.val_int = 0;
	
	return 0;
}// end of take_fconoff1
//****************************************************************************************************
static int8_t make_fconoff2(void* val)
{
	TParam *loc_prm = (TParam*)val;
	fc_ad_state_t loc_state = param[FC2AESTATE].value.val_int;
	
	if((loc_state == fc_ad_off) || (loc_state == fc_ad_on) || (loc_state == fc_ad_error)) loc_prm->value.val_int = 1;
	else loc_prm->value.val_int = 0;
	
	return 0;
}// end of take_fconoff2

//****************************************************************************************************
void init_params_bu()
{
	int8_t err = 0;

	// Метка времени
	static char parname_TIMESTAMP2[] = "TIME_STAMP2";
	param[TIMESTAMP2].name 	= parname_TIMESTAMP2;
	param[TIMESTAMP2].type 	= PARAM_TYPE_SECOND;
	param[TIMESTAMP2].read	= get_time_stamp;
	err = param_init(&param[TIMESTAMP2]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[TIMESTAMP2], param[TIMESTAMP2].name, 1);

	// Приказ оператора
	static char parname_OPERATORCOMMAND[] = "OPERATOR_COMMAND";
	param[OPERATORCOMMAND].name 	= parname_OPERATORCOMMAND;
	param[OPERATORCOMMAND].type 	= PARAM_TYPE_EXT_RENEW;
	// значение записывается вышестоящим кодом средствами адаптера данных
	err = param_init(&param[OPERATORCOMMAND]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	
	
	// Внешняя отладочная команда
	static char parname_EXTERNALCOMMAND[] = "EXTERNAL_COMMAND";
	param[EXTERNALCOMMAND].name 	= parname_EXTERNALCOMMAND;
	param[EXTERNALCOMMAND].type 	= PARAM_TYPE_EXT_RENEW;
	// значение записывается вышестоящим кодом средствами адаптера данных
	err = param_init(&param[EXTERNALCOMMAND]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	
//	static char parname_HMODE[] = "H_MODE";
//	param[HMODE].name 	= parname_HMODE;
//	param[HMODE].type 	= PARAM_TYPE_EXT_RENEW;
//	// значение записывается вышестоящим кодом средствами адаптера данных
//	err = param_init(&param[HMODE]);
//	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);

	// Адрес массива уставок в ОЗУ
	static char parname_ADDRPRESETRAM[] 	= "ADDR_PRESET_RAM2";
	param[ADDRPRESETRAM2].name 				= parname_ADDRPRESETRAM;
	param[ADDRPRESETRAM2].value.val_int 	= (uint32_t)(&preset[0]);

	// Адрес массива калибровок в ОЗУ
	static char parname_ADDRCALIBRRAM[] 	= "ADDR_CALIBR_RAM2";
	param[ADDRCALIBRRAM2].name 				= parname_ADDRCALIBRRAM;
	param[ADDRCALIBRRAM2].value.val_int 	= (uint32_t)(&coefs[0]);

	// Адрес массива уставок в ПЗУ
	static char parname_ADDRPRESETROM[] 	= "ADDR_PRESET_ROM2";
	param[ADDRPRESETROM2].name 				= parname_ADDRPRESETROM;
	param[ADDRPRESETROM2].value.val_int 	= PRESET_ADDR;

	// Адрес массива калибровок в ПЗУ
	static char parname_ADDRCALIBRROM[] 	= "ADDR_CALIBR_ROM2";
	param[ADDRCALIBRROM2].name 				= parname_ADDRCALIBRROM;
	param[ADDRCALIBRROM2].value.val_int 	= CALIBR_ADDR;

	// Адрес массива фильтров в ПЗУ
	static char parname_ADDRFILTRROM[] 		= "ADDR_FILTR_ROM2";
	param[ADDRFILTRROM2].name 				= parname_ADDRFILTRROM;
	param[ADDRFILTRROM2].value.val_int 		= FILTERS_SETT_ADDR;

	// Адрес массива фильтров в ОЗУ
	static char parname_ADDRFILTRRAM[] 		= "ADDR_FILTR_RAM2";
	param[ADDRFILTRRAM2].name 				= parname_ADDRFILTRRAM;
	param[ADDRFILTRRAM2].value.val_int 		= (uint32_t)filters_addresses_lengths;

	// Адрес наработки в ПЗУ
	static char parname_ADDRMOTOHOURS[] 	= "ADDR_MOTOHOURS2";
	param[ADDRMOTOHOURS2].name 				= parname_ADDRMOTOHOURS;
	param[ADDRMOTOHOURS2].value.val_int 	= MOTOHOURS_ADDR;
	
		
	// Адрес структуры режима в ОЗУ 
	static char parname_ADDRSTMODERAM3[]	= "ADDR_STMODE_RAM3";
	param[ADDRSTMODERAM3].name 				= parname_ADDRSTMODERAM3;
	param[ADDRSTMODERAM3].type 				= PARAM_TYPE_EXT_RENEW;
	param[ADDRSTMODERAM3].value.val_int 	= (uint32_t)(&(main_config_file.config_struct));	
	
	// Адрес структуры режима в ПЗУ
	static char parname_ADDRSTMODEFLASH3[]	= "ADDR_STMODE_FLASH3";
	param[ADDRSTMODEFLASH3].name 			= parname_ADDRSTMODEFLASH3;
	param[ADDRSTMODEFLASH3].type 			= PARAM_TYPE_EXT_RENEW;
	param[ADDRSTMODEFLASH3].value.val_int 	= SETTINGS_ADDR;	

	// Версия ПО модуля управления
	static char parname_SWVERSION[] 		= "SW_VERSION2";
	param[SWVERSION2].name 					= parname_SWVERSION;
	param[SWVERSION2].value.val_int 		= SOFTWARE_VERSION;

	// Команды БУ 50
	static char parname_COMMANDSBU50[] = "COMMANDS_BU_50";
	param[COMMANDSBU50].name 	= parname_COMMANDSBU50;
	param[COMMANDSBU50].type 	= PARAM_TYPE_SECOND;
	param[COMMANDSBU50].read 	= make_commands;
	err = param_init(&param[COMMANDSBU50]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[COMMANDSBU50], param[COMMANDSBU50].name, 1);

	// Донесения1 БУ 50
	static char parname_DISCRETES150[] = "DISCRETES1_50";
	param[DISCRETES150].name 	= parname_DISCRETES150;
	param[DISCRETES150].type 	= PARAM_TYPE_SECOND;
	param[DISCRETES150].addrr	= (uint32_t)(&param[DISCRETES150]);
	param[DISCRETES150].read   	= make_reports1;
	err = param_init(&param[DISCRETES150]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[DISCRETES150], param[DISCRETES150].name, 1);

	// Донесения2 БУ 50
	static char parname_DISCRETES250[] = "DISCRETES2_50";
	param[DISCRETES250].name 	= parname_DISCRETES250;
	param[DISCRETES250].type 	= PARAM_TYPE_SECOND;
	param[DISCRETES250].addrr	= (uint32_t)(&param[DISCRETES250]);
	param[DISCRETES250].read   	= make_reports2;
	err = param_init(&param[DISCRETES250]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[DISCRETES250], param[DISCRETES250].name, 1);

	// Запуск преобразований МАВ A4
	static char parname_POLLINGMAVA4[] = "POLLING_MAV_A4";
	param[POLLINGMAVA4].name 	= parname_POLLINGMAVA4;
	param[POLLINGMAVA4].read 	= polling_mav_a4;
	err = param_init(&param[POLLINGMAVA4]);
	if (err < 0)
	{
		debug_printf("%d error init param\n\r", __LINE__);
	}
	periodic_add_item(&params_periodic_A4, &param[POLLINGMAVA4], param[POLLINGMAVA4].name, 1);

	// Запуск преобразований МАВ A5
	static char parname_POLLINGMAVA5[] = "POLLING_MAV_A5";
	param[POLLINGMAVA5].name 	= parname_POLLINGMAVA5;
	param[POLLINGMAVA5].read 	= polling_mav_a5;
	err = param_init(&param[POLLINGMAVA5]);
	if (err < 0)
	{
		debug_printf("%d error init param\n\r", __LINE__);
	}
	periodic_add_item(&params_periodic_A5, &param[POLLINGMAVA5], param[POLLINGMAVA5].name, 1);

	// Запуск преобразований МАВ A6
	static char parname_POLLINGMAVA6[] = "POLLING_MAV_A6";
	param[POLLINGMAVA6].name 	= parname_POLLINGMAVA6;
	param[POLLINGMAVA6].read 	= polling_mav_a6;
	err = param_init(&param[POLLINGMAVA6]);
	if (err < 0)
	{
		debug_printf("%d error init param\n\r", __LINE__);
	}
	periodic_add_item(&params_periodic_A6, &param[POLLINGMAVA6], param[POLLINGMAVA6].name, 1);
	
	// Состояние КА А0
	static char parname_FSMA0STATE[] = "FSM_A0_STATE";
	param[FSMA0STATE].name 	= parname_FSMA0STATE;
	param[FSMA0STATE].type 	= PARAM_TYPE_EXT_RENEW;

	// Шапка уставок CRC
	static char parname_PRESETHEADERCRC2[] = "PRESET_HEADER_CRC2";
	param[PRESETHEADERCRC2].name 	= parname_PRESETHEADERCRC2;
	param[PRESETHEADERCRC2].value.val_int = PRESET_HEADER_CRC2;

	// Шапка уставок дата
	static char parname_PRESETHEADERDATE2[] = "PRESET_HEADER_DATE2";
	param[PRESETHEADERDATE2].name 	= parname_PRESETHEADERDATE2;
	param[PRESETHEADERDATE2].value.val_int = PRESET_HEADER_DATE2;

	// Шапка уставок время
	static char parname_PRESETHEADERTIME2[] = "PRESET_HEADER_TIME2";
	param[PRESETHEADERTIME2].name 	= parname_PRESETHEADERTIME2;
	param[PRESETHEADERTIME2].value.val_int = PRESET_HEADER_TIME2;

	// Шапка уставок git_commit
	static char parname_PRESETHEADERGITCOMMIT2[] = "PRESET_HEADER_GIT_COMMIT2";
	param[PRESETHEADERGITCOMMIT2].name 	= parname_PRESETHEADERGITCOMMIT2;
	param[PRESETHEADERGITCOMMIT2].value.val_int = PRESET_HEADER_GIT_COMMIT2;

	// Шапка уставок from display
	static char parname_PRESETHEADERFROMDISPLAY2[] = "PRESET_HEADER_FROM_DISPLAY2";
	param[PRESETHEADERFROMDISPLAY2].name 	= parname_PRESETHEADERFROMDISPLAY2;
	param[PRESETHEADERFROMDISPLAY2].value.val_int = PRESET_HEADER_FROM_DISPLAY2;

	// Шапка уставок длина данных в кол-ве struct
	static char parname_PRESETHEADERDATALENGTH2[] = "PRESET_HEADER_DATA_LENGTH2";
	param[PRESETHEADERDATALENGTH2].name 	= parname_PRESETHEADERDATALENGTH2;
	param[PRESETHEADERDATALENGTH2].value.val_int = PRESET_HEADER_DATA_LENGTH2;

	// Шапка калибровок CRC
	static char parname_CALIBRATIONHEADERCRC2[] = "CALIBRATION_HEADER_CRC2";
	param[CALIBRATIONHEADERCRC2].name 	= parname_CALIBRATIONHEADERCRC2;
	param[CALIBRATIONHEADERCRC2].value.val_int = CALIBRATION_HEADER_CRC2;

	// Шапка калибровок дата
	static char parname_CALIBRATIONHEADERDATE2[] = "CALIBRATION_HEADER_DATE2";
	param[CALIBRATIONHEADERDATE2].name 	= parname_CALIBRATIONHEADERDATE2;
	param[CALIBRATIONHEADERDATE2].value.val_int = CALIBRATION_HEADER_DATE2;

	// Шапка калибровок время
	static char parname_CALIBRATIONHEADERTIME2[] = "CALIBRATION_HEADER_TIME2";
	param[CALIBRATIONHEADERTIME2].name 	= parname_CALIBRATIONHEADERTIME2;
	param[CALIBRATIONHEADERTIME2].value.val_int = CALIBRATION_HEADER_TIME2;

	// Шапка калибровок git_commit
	static char parname_CALIBRATIONHEADERGITCOMMIT2[] = "CALIBRATION_HEADER_GIT_COMMIT2";
	param[CALIBRATIONHEADERGITCOMMIT2].name 	= parname_CALIBRATIONHEADERGITCOMMIT2;
	param[CALIBRATIONHEADERGITCOMMIT2].value.val_int = CALIBRATION_HEADER_GIT_COMMIT2;

	// Шапка калибровок from display
	static char parname_CALIBRATIONHEADERFROMDISPLAY2[] = "CALIBRATION_HEADER_FROM_DISPLAY2";
	param[CALIBRATIONHEADERFROMDISPLAY2].name 	= parname_CALIBRATIONHEADERFROMDISPLAY2;
	param[CALIBRATIONHEADERFROMDISPLAY2].value.val_int = CALIBRATION_HEADER_FROM_DISPLAY2;

	// Шапка калибровок длина данных в кол-ве struct
	static char parname_CALIBRATIONHEADERDATALENGTH2[] = "CALIBRATION_HEADER_DATA_LENGTH2";
	param[CALIBRATIONHEADERDATALENGTH2].name 	= parname_CALIBRATIONHEADERDATALENGTH2;
	param[CALIBRATIONHEADERDATALENGTH2].value.val_int = CALIBRATION_HEADER_DATA_LENGTH2;

	// Шапка фильтров CRC
	static char parname_FILTERHEADERCRC2[] = "FILTER_HEADER_CRC2";
	param[FILTERHEADERCRC2].name 	= parname_FILTERHEADERCRC2;
	param[FILTERHEADERCRC2].value.val_int = FILTER_HEADER_CRC2;

	// Шапка фильтров дата
	static char parname_FILTERHEADERDATE2[] = "FILTER_HEADER_DATE2";
	param[FILTERHEADERDATE2].name 	= parname_FILTERHEADERDATE2;
	param[FILTERHEADERDATE2].value.val_int = FILTER_HEADER_DATE2;

	// Шапка фильтров время
	static char parname_FILTERHEADERTIME2[] = "FILTER_HEADER_TIME2";
	param[FILTERHEADERTIME2].name 	= parname_FILTERHEADERTIME2;
	param[FILTERHEADERTIME2].value.val_int = FILTER_HEADER_TIME2;

	// Шапка фильтров git_commit
	static char parname_FILTERHEADERGITCOMMIT2[] = "FILTER_HEADER_GIT_COMMIT2";
	param[FILTERHEADERGITCOMMIT2].name 	= parname_FILTERHEADERGITCOMMIT2;
	param[FILTERHEADERGITCOMMIT2].value.val_int = FILTER_HEADER_GIT_COMMIT2;

	// Шапка фильтров from display
	static char parname_FILTERHEADERFROMDISPLAY2[] = "FILTER_HEADER_FROM_DISPLAY2";
	param[FILTERHEADERFROMDISPLAY2].name 	= parname_FILTERHEADERFROMDISPLAY2;
	param[FILTERHEADERFROMDISPLAY2].value.val_int = FILTER_HEADER_FROM_DISPLAY2;

	// Шапка фильтров длина данных в кол-ве struct
	static char parname_FILTERHEADERDATALENGTH2[] = "FILTER_HEADER_DATA_LENGTH2";
	param[FILTERHEADERDATALENGTH2].name 	= parname_FILTERHEADERDATALENGTH2;
	param[FILTERHEADERDATALENGTH2].value.val_int = FILTER_HEADER_DATA_LENGTH2;
	
	
	// Индикация режима запуска ПЧ100 1
	static char parname_FC1STARTING[] = "FC1_STARTING";
	param[FC1STARTING].name 	= parname_FC1STARTING;
	param[FC1STARTING].type 	= PARAM_TYPE_SECOND;
	param[FC1STARTING].read 	= make_fcstarting1;
	err = param_init(&param[FC1STARTING]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[FC1STARTING], param[FC1STARTING].name, 1);
	
	// Индикация режима запуска ПЧ100 2
	static char parname_FC2STARTING[]	= "FC2_STARTING";
	param[FC2STARTING].name 			= parname_FC2STARTING;
	param[FC2STARTING].type 			= PARAM_TYPE_SECOND;
	param[FC2STARTING].read 			= make_fcstarting2;
	err = param_init(&param[FC2STARTING]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[FC2STARTING], param[FC2STARTING].name, 1);
	
	// Индикация режима останова ПЧ100 1
	static char parname_FC1ONOFF[]		= "FC1_ON_OFF";
	param[FC1ONOFF].name 				= parname_FC1ONOFF;
	param[FC1ONOFF].type 				= PARAM_TYPE_SECOND;
	param[FC1ONOFF].read 				= make_fconoff1;
	err = param_init(&param[FC1ONOFF]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[FC1ONOFF], param[FC1ONOFF].name, 1);
	
	// Индикация режима останова ПЧ100 2
	static char parname_FC2ONOFF[]	= "FC2_ON_OFF";
	param[FC2ONOFF].name 			= parname_FC2ONOFF;
	param[FC2ONOFF].type 			= PARAM_TYPE_SECOND;
	param[FC2ONOFF].read 			= make_fconoff2;
	err = param_init(&param[FC2ONOFF]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[FC2ONOFF], param[FC2ONOFF].name, 1);

	// Составной параметр аварий БУ50
	static char parname_EVENTSBLOCK50[] = "EVENTS_BLOCK_50";
	param[EVENTSBLOCK50].name 	= parname_EVENTSBLOCK50;
	param[EVENTSBLOCK50].type 	= PARAM_TYPE_EXT_RENEW;
	param[EVENTSBLOCK50].read 		= make_events_bu_50;
	err = param_init(&param[EVENTSBLOCK50]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[EVENTSBLOCK50], param[EVENTSBLOCK50].name, 1);	
	
}//end of init_params_bu

void init_params_ur400()
{

	// Автомат фидера 3
	static char parname_FID3AUT[] = "FID3_AUT";
	init_discrete(FID3AUT, MODULES_50_A7, DISCR_CH_16, parname_FID3AUT, 1);

	// Автомат фидера 3 включен
	static char parname_FID3AUTOP[] = "FID3_AUT_OP";
	init_discrete(FID3AUTOP, MODULES_50_A7, DISCR_CH_15, parname_FID3AUTOP, 5);

	// Контактор фидера 3
	static char parname_FID3CONT[] = "FID3_CONT";
	init_discrete(FID3CONT, MODULES_50_A8, DISCR_CH_08, parname_FID3CONT, 1);

	// Автомат фидера 3-1
	static char parname_FID31AUT[] = "FID3_1_AUT";
	init_discrete(FID31AUT, MODULES_50_A7, DISCR_CH_14, parname_FID31AUT, 5);

	// Автомат фидера 3-1 включен
	static char parname_FID31AUTOP[] = "FID3_1_AUT_OP";
	init_discrete(FID31AUTOP, MODULES_50_A7, DISCR_CH_13, parname_FID31AUTOP, 5);

	// Контактор фидера 3-1
	static char parname_FID31CONT[] = "FID3_1_CONT";
	init_discrete(FID31CONT, MODULES_50_A8, DISCR_CH_07, parname_FID31CONT, 1);

	// Автомат фидера 3-2
	static char parname_FID32AUT[] = "FID3_2_AUT";
	init_discrete(FID32AUT, MODULES_50_A9, DISCR_CH_14, parname_FID32AUT, 5);

	// Автомат фидера 3-2 включен
	static char parname_FID32AUTOP[] = "FID3_2_AUT_OP";
	init_discrete(FID32AUTOP, MODULES_50_A9, DISCR_CH_13, parname_FID32AUTOP, 5);

	// Контактор фидера 3-2
	static char parname_FID32CONT[] = "FID3_2_CONT";
	init_discrete(FID32CONT, MODULES_50_A9, DISCR_CH_06, parname_FID32CONT, 1);

	// Автомат фидера 4
	static char parname_FID4AUT[] = "FID4_AUT";
	init_discrete(FID4AUT, MODULES_50_A9, DISCR_CH_16, parname_FID4AUT, 5);

	// Автомат фидера 4 включен
	static char parname_FID4AUTOP[] = "FID4_AUT_OP";
	init_discrete(FID4AUTOP, MODULES_50_A9, DISCR_CH_15, parname_FID4AUTOP, 5);

	// Контактор фидера 4
	static char parname_FID4CONT[] = "FID4_CONT";
	init_discrete(FID4CONT, MODULES_50_A9, DISCR_CH_07, parname_FID4CONT, 1);

	// Автомат трансформатора
	static char parname_TRANSAUT[] = "TRANS_AUT";
	init_discrete(TRANSAUT, MODULES_50_A7, DISCR_CH_20, parname_TRANSAUT, 5);

	// Автомат трансформатора включен
	static char parname_TRANSAUTOP[] = "TRANS_AUT_OP";
	init_discrete(TRANSAUTOP, MODULES_50_A7, DISCR_CH_19, parname_TRANSAUTOP, 5);

	// Автомат трансформатора
	static char parname_TRANS2AUT[] = "TRANS2_AUT";
	init_discrete(TRANS2AUT, MODULES_50_A7, DISCR_CH_22, parname_TRANS2AUT, 5);

	// Автомат трансформатора включен
	static char parname_TRANS2AUTOP[] = "TRANS2_AUT_OP";
	init_discrete(TRANS2AUTOP, MODULES_50_A7, DISCR_CH_21, parname_TRANS2AUTOP, 5);

	// Контактор вентиляторов
	static char parname_VENTCONT[] = "VENT_CONT";
	init_discrete(VENTCONT, MODULES_50_A9, DISCR_CH_17, parname_VENTCONT, 1);
}// end of init_params_ur400
//****************************************************************************************************
void init_params_ur230()
{

	// Автомат фидера 1
	static char parname_FID1AUT[] = "FID1_AUT";
	init_discrete(FID1AUT, MODULES_50_A7, DISCR_CH_18, parname_FID1AUT, 1);

	// Автомат фидера 1 включен
	static char parname_FID1AUTOP[] = "FID1_AUT_OP";
	init_discrete(FID1AUTOP, MODULES_50_A7, DISCR_CH_17, parname_FID1AUTOP, 1);

	// Контактор фидера 1
	static char parname_FID1CONT[] = "FID1_CONT";
	init_discrete(FID1CONT, MODULES_50_A8, DISCR_CH_09, parname_FID1CONT, 1);

	// Контактор фидера 2
	static char parname_FID2CONT[] = "FID2_CONT";
	init_discrete(FID2CONT, MODULES_50_A9, DISCR_CH_08, parname_FID2CONT, 1);

}// end of init_params_ur230
//****************************************************************************************************
void init_params_ur27()
{

	int8_t err = 0;
	
    // Режим работы люка выброса
    static char parname_HMODE2[] = "H_MODE_2";
	param[HMODE2].name 	= parname_HMODE2;
	param[HMODE2].type 	= PARAM_TYPE_EXT_RENEW;
	// значение записывается вышестоящим кодом средствами адаптера данных
	err = param_init(&param[HMODE2]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);

	// Ручное управление вентиляторами
	static char parname_VENTMANUAL[] = "VENT_MANUAL";
	init_discrete(VENTMANUAL, MODULES_50_A9, DISCR_CH_18, parname_VENTMANUAL, 5);

	// Автоматическое управление вентиляторами
	static char parname_VENTAUTOMATIC[] = "VENT_AUTOMATIC";
	init_discrete(VENTAUTOMATIC, MODULES_50_A9, DISCR_CH_19, parname_VENTAUTOMATIC, 5);

}// end of init_params_ur27
//****************************************************************************************************
void init_params_fuel_pump()
{
	// ДНУТ залит
	static char parname_LOWFUEL[] = "LOW_FUEL";
	init_discrete(LOWFUEL, MODULES_50_A7, DISCR_CH_03, parname_LOWFUEL, 5);

	// Внешний ДНУТ залит
	static char parname_LOWEXTFUEL[] = "LOW_EXT_FUEL";
	init_discrete(LOWEXTFUEL, MODULES_50_A7, DISCR_CH_09, parname_LOWEXTFUEL, 5);

}// end of init_params_ur27
//****************************************************************************************************
void init_params_hatches()
{
	int8_t err = 0;

	// Агрегат Люк 5

    // Состояние люка выброса 1
	static char parname_HATCH5STATE[] = "HATCH_5_STATE";
	param[HATCH5STATE].name 	= parname_HATCH5STATE;
	param[HATCH5STATE].type 	= PARAM_TYPE_EXT_RENEW;
	// значение записывается вышестоящим кодом средствами адаптера данных
	err = param_init(&param[HATCH5STATE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);

    // Отказ люка выброса 1. Устанавливается в 1 в случае отказа люка.
	static char parname_HATCH5BREAK[] = "HATCH_5_BREAK";
	param[HATCH5BREAK].name 	= parname_HATCH5BREAK;
	param[HATCH5BREAK].type 	= PARAM_TYPE_EXT_RENEW;
	// значение записывается вышестоящим кодом средствами адаптера данных
	err = param_init(&param[HATCH5BREAK]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);


	// Люк открыт
	static char parname_OH5[] = "O_H_5";
	init_discrete(OH5, MODULES_50_A8, DISCR_CH_16, parname_OH5, 5);

	// Люк закрыт
	static char parname_CH5[] = "C_H_5";
	init_discrete(CH5, MODULES_50_A8, DISCR_CH_15, parname_CH5, 5);

	// Включено реле открывания люка
	static char parname_ONOH5[] = "ON_O_H_5";
	init_discrete(ONOH5, MODULES_50_A8, DISCR_CH_14, parname_ONOH5, 5);

	// Включено реле закрывания люка
	static char parname_ONCH5[] = "ON_C_H_5";
	init_discrete(ONCH5, MODULES_50_A8, DISCR_CH_13, parname_ONCH5, 5);

	// Агрегат Люк 6

    // Состояние люка выброса 2
	static char parname_HATCH6STATE[] = "HATCH_6_STATE";
	param[HATCH6STATE].name 	= parname_HATCH6STATE;
	param[HATCH6STATE].type 	= PARAM_TYPE_EXT_RENEW;
	// значение записывается вышестоящим кодом средствами адаптера данных
	err = param_init(&param[HATCH6STATE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);

    // Отказ люка выброса 2. Устанавливается в 1 в случае отказа люка.
	static char parname_HATCH6BREAK[] = "HATCH_6_BREAK";
	param[HATCH6BREAK].name 	= parname_HATCH6BREAK;
	param[HATCH6BREAK].type 	= PARAM_TYPE_EXT_RENEW;
	// значение записывается вышестоящим кодом средствами адаптера данных
	err = param_init(&param[HATCH6BREAK]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);

	// Люк открыт
	static char parname_OH6[] = "O_H_6";
	init_discrete(OH6, MODULES_50_A9, DISCR_CH_23, parname_OH6, 5);

	// Люк закрыт
	static char parname_CH6[] = "C_H_6";
	init_discrete(CH6, MODULES_50_A9, DISCR_CH_22, parname_CH6, 5);

	// Включено реле открывания люка
	static char parname_ONOH6[] = "ON_O_H_6";
	init_discrete(ONOH6, MODULES_50_A9, DISCR_CH_21, parname_ONOH6, 5);

	// Включено реле закрывания люка
	static char parname_ONCH6[] = "ON_C_H_6";
	init_discrete(ONCH6, MODULES_50_A9, DISCR_CH_20, parname_ONCH6, 5);

}// end of init_params_hatches
//****************************************************************************************************
void init_params_fc1()
{
	int8_t err = 0;

	//TODO
	// Для теста пуска ПЧ отключил фильтрацию токов. После теста вернуть!
	
	// I АД фазы А
	static char parname_FC1AEIA[]		= "FC1_AE_I_A";
	param[FC1AEIA].name 				= parname_FC1AEIA;
	param[FC1AEIA].type 				= PARAM_TYPE_ANALOG;
	param[FC1AEIA].module 				= &module[MODULES_50_A6];
	param[FC1AEIA].addrr 				= MOD380_ADDR_RMS + MOD380_CH_01;
	param[FC1AEIA].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[FC1AEIA].coef 			= &coefs[FC1_AE_I_A_k];
	mas_calibr[FC1AEIA].calibr 			= param_calibr_line_1_positive;
	param[FC1AEIA].calibr_obj			= &mas_calibr[FC1AEIA];
	// Фильтр скользящим средним
	param[FC1AEIA].filter_obj.filter_type 		= f_no_filter;
	param[FC1AEIA].filter_obj.filter_ptr.fma	= &FC1_AE_I_A_FILTER;
	err = param_init(&param[FC1AEIA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[FC1AEIA], param[FC1AEIA].name, 1);

	// I АД фазы B
	static char parname_FC1AEIB[]		= "FC1_AE_I_B";
	param[FC1AEIB].name 					= parname_FC1AEIB;
	param[FC1AEIB].type 					= PARAM_TYPE_ANALOG;
	param[FC1AEIB].module 				= &module[MODULES_50_A6];
	param[FC1AEIB].addrr 				= MOD380_ADDR_RMS + MOD380_CH_02;
	param[FC1AEIB].read 					= mod380_read;
	//Линейная аппроксимация
	mas_calibr[FC1AEIB].coef 			= &coefs[FC1_AE_I_B_k];
	mas_calibr[FC1AEIB].calibr 			= param_calibr_line_1_positive;
	param[FC1AEIB].calibr_obj			= &mas_calibr[FC1AEIB];
	// Фильтр скользящим средним
	param[FC1AEIB].filter_obj.filter_type 		= f_no_filter;
	param[FC1AEIB].filter_obj.filter_ptr.fma	= &FC1_AE_I_B_FILTER;
	err = param_init(&param[FC1AEIB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[FC1AEIB], param[FC1AEIB].name, 1);

	// I АД фазы C
	static char parname_FC1AEIC[]		= "FC1_AE_I_C";
	param[FC1AEIC].name 					= parname_FC1AEIC;
	param[FC1AEIC].type 					= PARAM_TYPE_ANALOG;
	param[FC1AEIC].module 				= &module[MODULES_50_A6];
	param[FC1AEIC].addrr 				= MOD380_ADDR_RMS + MOD380_CH_03;
	param[FC1AEIC].read 					= mod380_read;
	//Линейная аппроксимация
	mas_calibr[FC1AEIC].coef 			= &coefs[FC1_AE_I_C_k];
	mas_calibr[FC1AEIC].calibr 			= param_calibr_line_1_positive;
	param[FC1AEIC].calibr_obj			= &mas_calibr[FC1AEIC];
	// Фильтр скользящим средним
	param[FC1AEIC].filter_obj.filter_type 		= f_no_filter;
	param[FC1AEIC].filter_obj.filter_ptr.fma	= &FC1_AE_I_C_FILTER;
	err = param_init(&param[FC1AEIC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[FC1AEIC], param[FC1AEIC].name, 1);

	// Угол I АД фазы А
	static char parname_FC1AEPHIIA[]		= "FC1_AE_PHI_I_A";
	param[FC1AEPHIIA].name 				= parname_FC1AEPHIIA;
	param[FC1AEPHIIA].type 				= PARAM_TYPE_ANALOG;
	param[FC1AEPHIIA].module 			= &module[MODULES_50_A6];
	param[FC1AEPHIIA].addrr 				= MOD380_ADDR_PHASE + MOD380_CH_01;
	param[FC1AEPHIIA].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[FC1AEPHIIA].coef 			= 0;
	mas_calibr[FC1AEPHIIA].calibr 		= param_calibr_none;
	param[FC1AEPHIIA].calibr_obj			= &mas_calibr[FC1AEPHIIA];
	// Фильтр скользящим средним
	param[FC1AEPHIIA].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[FC1AEPHIIA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[FC1AEPHIIA], param[FC1AEPHIIA].name, 10);

	// Угол I АД фазы B
	static char parname_FC1AEPHIIB[]		= "FC1_AE_PHI_I_B";
	param[FC1AEPHIIB].name 				= parname_FC1AEPHIIB;
	param[FC1AEPHIIB].type 				= PARAM_TYPE_ANALOG;
	param[FC1AEPHIIB].module 			= &module[MODULES_50_A6];
	param[FC1AEPHIIB].addrr 				= MOD380_ADDR_PHASE + MOD380_CH_02;
	param[FC1AEPHIIB].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[FC1AEPHIIB].coef 			= 0;
	mas_calibr[FC1AEPHIIB].calibr 		= param_calibr_none;
	param[FC1AEPHIIB].calibr_obj			= &mas_calibr[FC1AEPHIIB];
	// Фильтр скользящим средним
	param[FC1AEPHIIB].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[FC1AEPHIIB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[FC1AEPHIIB], param[FC1AEPHIIB].name, 10);

	// Угол I АД фазы C
	static char parname_FC1AEPHIIC[]		= "FC1_AE_PHI_I_C";
	param[FC1AEPHIIC].name 				= parname_FC1AEPHIIC;
	param[FC1AEPHIIC].type 				= PARAM_TYPE_ANALOG;
	param[FC1AEPHIIC].module 			= &module[MODULES_50_A6];
	param[FC1AEPHIIC].addrr 				= MOD380_ADDR_PHASE + MOD380_CH_03;
	param[FC1AEPHIIC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[FC1AEPHIIC].coef 			= 0;
	mas_calibr[FC1AEPHIIC].calibr 		= param_calibr_none;
	param[FC1AEPHIIC].calibr_obj			= &mas_calibr[FC1AEPHIIC];
	// Фильтр скользящим средним
	param[FC1AEPHIIC].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[FC1AEPHIIC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A6, &param[FC1AEPHIIC], param[FC1AEPHIIC].name, 10);

	// Контактор питания АД ПЧ
	static char parname_AEFC1CONT[] = "AE_FC1_CONT";
	init_discrete(AEFC1CONT, MODULES_50_A8, DISCR_CH_03, parname_AEFC1CONT, 1);

	// Контактор питания АД ПЧ треугольником
	static char parname_AEFC1TRIANGLECONT[] = "AE_FC1_TRIANGLE_CONT";
	init_discrete(AEFC1TRIANGLECONT, MODULES_50_A8, DISCR_CH_04, parname_AEFC1TRIANGLECONT, 1);

	// Контактор питания АД ПЧ звездой
	static char parname_AEFC1STARCONT[] = "AE_F1C_STAR_CONT";
	init_discrete(AEFC1STARCONT, MODULES_50_A8, DISCR_CH_05, parname_AEFC1STARCONT, 1);

	// Состояние ПЧ
	static char parname_FC1AESTATE[] = "FC1_AE_STATE";
	param[FC1AESTATE].name 	= parname_FC1AESTATE;
	param[FC1AESTATE].type 	= PARAM_TYPE_EXT_RENEW;
	err = param_init(&param[FC1AESTATE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	
	// Составной параметр аварий ПЧ1 БУ50
	static char parname_EVENTSFC150[] = "EVENTS_FC1_50";
	param[EVENTSFC150].name 	= parname_EVENTSFC150;
	param[EVENTSFC150].type 	= PARAM_TYPE_EXT_RENEW;
	param[EVENTSFC150].read 		= make_events_fc_50;
	err = param_init(&param[EVENTSFC150]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic, &param[EVENTSFC150], param[EVENTSFC150].name, 1);
	

    // Наработка ПЧ1
	static char parname_FC1MOTOHOURS[] = "FC1_MOTOHOURS";
	param[FC1MOTOHOURS].name 	= parname_FC1MOTOHOURS;
	param[FC1MOTOHOURS].type 	= PARAM_TYPE_SECOND;
	param[FC1MOTOHOURS].addrr 	= 0;
	param[FC1MOTOHOURS].read 	= calc_fc1_motohours;
	err = param_init(&param[FC1MOTOHOURS]);
	periodic_add_item(&params_periodic, &param[FC1MOTOHOURS], param[FC1MOTOHOURS].name,	100);

    // Наработка ПЧ1 в часах
	static char parname_FC1HOURS[] = "FC1_HOURS";
	param[FC1HOURS].name 	= parname_FC1HOURS;
	param[FC1HOURS].type 	= PARAM_TYPE_SECOND;
	param[FC1HOURS].addrr 	= FC1MOTOHOURS;
	param[FC1HOURS].read 	= calc_hours;
	err = param_init(&param[FC1HOURS]);
	periodic_add_item(&params_periodic, &param[FC1HOURS], param[FC1HOURS].name,	100);

}// end of init_params_fc
//****************************************************************************************************
void init_params_fc2()
{
	int8_t err = 0;

	// I АД фазы А
	static char parname_FC2AEIA[]		= "FC2_AE_I_A";
	param[FC2AEIA].name 				= parname_FC2AEIA;
	param[FC2AEIA].type 				= PARAM_TYPE_ANALOG;
	param[FC2AEIA].module 				= &module[MODULES_50_A5];
	param[FC2AEIA].addrr 				= MOD380_ADDR_RMS + MOD380_CH_10;
	param[FC2AEIA].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[FC2AEIA].coef 			= &coefs[FC2_AE_I_A_k];
	mas_calibr[FC2AEIA].calibr 			= param_calibr_line_1_positive;
	param[FC2AEIA].calibr_obj			= &mas_calibr[FC2AEIA];
	// Фильтр скользящим средним
	param[FC2AEIA].filter_obj.filter_type 		= f_no_filter;
	param[FC2AEIA].filter_obj.filter_ptr.fma	= &FC2_AE_I_A_FILTER;
	err = param_init(&param[FC2AEIA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[FC2AEIA], param[FC2AEIA].name, 1);

	// I АД фазы B
	static char parname_FC2AEIB[]		= "FC2_AE_I_B";
	param[FC2AEIB].name 				= parname_FC2AEIB;
	param[FC2AEIB].type 				= PARAM_TYPE_ANALOG;
	param[FC2AEIB].module 				= &module[MODULES_50_A5];
	param[FC2AEIB].addrr 				= MOD380_ADDR_RMS + MOD380_CH_11;
	param[FC2AEIB].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[FC2AEIB].coef 			= &coefs[FC2_AE_I_B_k];
	mas_calibr[FC2AEIB].calibr 			= param_calibr_line_1_positive;
	param[FC2AEIB].calibr_obj			= &mas_calibr[FC2AEIB];
	// Фильтр скользящим средним
	param[FC2AEIB].filter_obj.filter_type 		= f_no_filter;
	param[FC2AEIB].filter_obj.filter_ptr.fma	= &FC2_AE_I_B_FILTER;
	err = param_init(&param[FC2AEIB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[FC2AEIB], param[FC2AEIB].name, 1);

	// I АД фазы C
	static char parname_FC2AEIC[]		= "FC2_AE_I_C";
	param[FC2AEIC].name 				= parname_FC2AEIC;
	param[FC2AEIC].type 				= PARAM_TYPE_ANALOG;
	param[FC2AEIC].module 				= &module[MODULES_50_A5];
	param[FC2AEIC].addrr 				= MOD380_ADDR_RMS + MOD380_CH_12;
	param[FC2AEIC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[FC2AEIC].coef 			= &coefs[FC2_AE_I_C_k];
	mas_calibr[FC2AEIC].calibr 			= param_calibr_line_1_positive;
	param[FC2AEIC].calibr_obj			= &mas_calibr[FC2AEIC];
	// Фильтр скользящим средним
	param[FC2AEIC].filter_obj.filter_type 		= f_no_filter;
	param[FC2AEIC].filter_obj.filter_ptr.fma	= &FC2_AE_I_C_FILTER;
	err = param_init(&param[FC2AEIC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[FC2AEIC], param[FC2AEIC].name, 1);

	// Угол I АД фазы А
	static char parname_FC2AEPHIIA[]	= "FC2_AE_PHI_I_A";
	param[FC2AEPHIIA].name 				= parname_FC2AEPHIIA;
	param[FC2AEPHIIA].type 				= PARAM_TYPE_ANALOG;
	param[FC2AEPHIIA].module 			= &module[MODULES_50_A5];
	param[FC2AEPHIIA].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_10;
	param[FC2AEPHIIA].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[FC2AEPHIIA].coef 		= 0;
	mas_calibr[FC2AEPHIIA].calibr 		= param_calibr_none;
	param[FC2AEPHIIA].calibr_obj		= &mas_calibr[FC2AEPHIIA];
	// Фильтр скользящим средним
	param[FC2AEPHIIA].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[FC2AEPHIIA]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[FC2AEPHIIA], param[FC2AEPHIIA].name, 10);

	// Угол I АД фазы B
	static char parname_FC2AEPHIIB[]	= "FC2_AE_PHI_I_B";
	param[FC2AEPHIIB].name 				= parname_FC2AEPHIIB;
	param[FC2AEPHIIB].type 				= PARAM_TYPE_ANALOG;
	param[FC2AEPHIIB].module 			= &module[MODULES_50_A5];
	param[FC2AEPHIIB].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_11;
	param[FC2AEPHIIB].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[FC2AEPHIIB].coef 		= 0;
	mas_calibr[FC2AEPHIIB].calibr 		= param_calibr_none;
	param[FC2AEPHIIB].calibr_obj		= &mas_calibr[FC2AEPHIIB];
	// Фильтр скользящим средним
	param[FC2AEPHIIB].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[FC2AEPHIIB]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[FC2AEPHIIB], param[FC2AEPHIIB].name, 10);

	// Угол I АД фазы C
	static char parname_FC2AEPHIIC[]	= "FC2_AE_PHI_I_C";
	param[FC2AEPHIIC].name 				= parname_FC2AEPHIIC;
	param[FC2AEPHIIC].type 				= PARAM_TYPE_ANALOG;
	param[FC2AEPHIIC].module 			= &module[MODULES_50_A5];
	param[FC2AEPHIIC].addrr 			= MOD380_ADDR_PHASE + MOD380_CH_12;
	param[FC2AEPHIIC].read 				= mod380_read;
	//Линейная аппроксимация
	mas_calibr[FC2AEPHIIC].coef 		= 0;
	mas_calibr[FC2AEPHIIC].calibr 		= param_calibr_none;
	param[FC2AEPHIIC].calibr_obj		= &mas_calibr[FC2AEPHIIC];
	// Фильтр скользящим средним
	param[FC2AEPHIIC].filter_obj.filter_type 	= f_no_filter;
	err = param_init(&param[FC2AEPHIIC]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	periodic_add_item(&params_periodic_A5, &param[FC2AEPHIIC], param[FC2AEPHIIC].name, 10);

	// Контактор питания АД ПЧ2
	static char parname_AEFC2CONT[] = "AE_FC2_CONT";
	init_discrete(AEFC2CONT, MODULES_50_A9, DISCR_CH_03, parname_AEFC2CONT, 1);

	// Контактор питания АД ПЧ2 треугольником
	static char parname_AEFC2TRIANGLECONT[] = "AE_FC2_TRIANGLE_CONT";
	init_discrete(AEFC2TRIANGLECONT, MODULES_50_A9, DISCR_CH_04, parname_AEFC2TRIANGLECONT, 1);

	// Контактор питания АД ПЧ2 звездой
	static char parname_AEFC2STARCONT[] = "AE_FC2_STAR_CONT";
	init_discrete(AEFC2STARCONT, MODULES_50_A9, DISCR_CH_05, parname_AEFC2STARCONT, 1);

	// Состояние ПЧ2
	static char parname_FC2AESTATE[] = "FC2_AD_STATE";
	param[FC2AESTATE].name 	= parname_FC2AESTATE;
	param[FC2AESTATE].type 	= PARAM_TYPE_EXT_RENEW;
	err = param_init(&param[FC2AESTATE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	
    // Наработка ПЧ2
	static char parname_FC2MOTOHOURS[] = "FC2_MOTOHOURS";
	param[FC2MOTOHOURS].name 	= parname_FC2MOTOHOURS;
	param[FC2MOTOHOURS].type 	= PARAM_TYPE_SECOND;
	param[FC2MOTOHOURS].addrr 	= 0;
	param[FC2MOTOHOURS].read 	= calc_fc2_motohours;
	err = param_init(&param[FC2MOTOHOURS]);
	periodic_add_item(&params_periodic, &param[FC2MOTOHOURS], param[FC2MOTOHOURS].name,	100);

    // Наработка ПЧ2 в часах
	static char parname_FC2HOURS[] = "FC2_HOURS";
	param[FC2HOURS].name 	= parname_FC2HOURS;
	param[FC2HOURS].type 	= PARAM_TYPE_SECOND;
	param[FC2HOURS].addrr 	= FC2MOTOHOURS;
	param[FC2HOURS].read 	= calc_hours;
	err = param_init(&param[FC2HOURS]);
	periodic_add_item(&params_periodic, &param[FC2HOURS], param[FC2HOURS].name,	100);

}// end of init_params_fc2
//****************************************************************************************************
void init_extern_params()
{
	int8_t err = 0;

    // Выбран бак внешний
    static char parname_NZTSELECTEDTANK[]    	= "NZT_SELECTED_TANK";
	param[NZTSELECTEDTANK].name 				= parname_NZTSELECTEDTANK;
	param[NZTSELECTEDTANK].type 				= PARAM_TYPE_EXT_RENEW;
	err = param_init(&param[NZTSELECTEDTANK]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	
	//Режим управления станцией СЭC200М
	static char parname_STATIONCONTROLMODE[] 	= "STATION_CONTROL_MODE";
	param[STATIONCONTROLMODE].name 				= parname_STATIONCONTROLMODE;
	param[STATIONCONTROLMODE].type 				= PARAM_TYPE_EXT_RENEW;
	err = param_init(&param[STATIONCONTROLMODE]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	
	// Донесения1 БУ 400
	static char parname_DISCRETES400[] 			= "DISCRETES_400";
	param[DISCRETES400].name 					= parname_DISCRETES400;
	param[DISCRETES400].type 					= PARAM_TYPE_EXT_RENEW;
	err = param_init(&param[DISCRETES400]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	
	// Донесения2 БУ 400
	static char parname_DISCRETES2400[] 		= "DISCRETES2_400";
	param[DISCRETES2400].name 					= parname_DISCRETES2400;
	param[DISCRETES2400].type 					= PARAM_TYPE_EXT_RENEW;
	err = param_init(&param[DISCRETES2400]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	
	// Донесения1 БУ СЭС
	static char parname_DISCRETES1SES[] 		= "DISCRETES1_SES";
	param[DISCRETES1SES].name 					= parname_DISCRETES1SES;
	param[DISCRETES1SES].type 					= PARAM_TYPE_EXT_RENEW;
	err = param_init(&param[DISCRETES1SES]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	
	// Донесения2 БУ СЭС
	static char parname_DISCRETES2SES[] 		= "DISCRETES2_SES";
	param[DISCRETES2SES].name 					= parname_DISCRETES2SES;
	param[DISCRETES2SES].type 					= PARAM_TYPE_EXT_RENEW;
	err = param_init(&param[DISCRETES2SES]);
	if(err<0) debug_printf("%s %d !!error param\n\r", "params.c", __LINE__);
	
}// end of init_extern_params
//****************************************************************************************************
/**
 *  @brief Инициализация параметров.
 *  @details Инициализирует объекты всех параметров,
 *  	добавляет их в список для обновления.
 */
void init_params()
{
	int8_t err = 0;

	debug_printf("# init_params()\n");
	debug_printf("## Read presets\n");

//****************************************************************************************************	
// Чтение уставок из ПЗУ. Каждая уставка содержит 4 32-разрядных поля.
//****************************************************************************************************	
	set_MPORT_35_MHz();
	err = memory_read_settings_w_header(preset, (void *)(PRESET_ADDR),
										PRESET_NAMES_COUNTER << 4,
										&preset_header);

	if (err < 0)
	{
		debug_printf("%s %d Attention!!! Error while reading preset\n\r",
					 __FILE__, __LINE__);
		debug_printf("!!!Stop!!!\n\r");
		while (1)
			;
	}

	debug_printf("crc: %#x\n\r", preset_header.crc);
	debug_printf("date: %#x\n\r", preset_header.date);
	debug_printf("time: %#x\n\r", preset_header.time);
	debug_printf("git_commit: %#x\n\r", preset_header.git_commit);
	debug_printf("from_display: %d\n\r", preset_header.from_display);
	debug_printf("data_length: %d\n\r", preset_header.data_length);
	uint32_t preset_crc = crc32b(preset, PRESET_NAMES_COUNTER << 4);

	if (preset_crc != preset_header.crc)
	{
		debug_printf("%s %d Attention!!! Preset CRC check failed\n\r"
					 "Calculated CRC:%#x\n\rCRC from file: %#x\n\r",
					 __FILE__, __LINE__, preset_crc, preset_header.crc);
		debug_printf("!!!Stop!!!\n\r");
		while (1)
			;
	}
	else
	{
		debug_printf("CRC check OK\n\r");
	}

	// for (uint32_t index1 = 0; index1 < PRESET_NAMES_COUNTER; index1++)
	// {
	// 	debug_printf("%s %d: %d ps %x %x %x %x\n\r", __FILE__, __LINE__,
	// 				 index1, preset[index1].min_value.val_int,
	// 				 preset[index1].default_value.val_int,
	// 				 preset[index1].cur_value.val_int,
	// 				 preset[index1].max_value.val_int);
	// }

	debug_printf("\n## Read calibrations\n");
	// Чтение калибровочных коэффициентов из ПЗУ. Калибровки - вещественные
	// числа
	err = memory_read_settings_w_header(coefs, (void *)(CALIBR_ADDR),
										CALIBRATION_NAMES_COUNTER << 2,
										&calibration_header);

	// for (index1 = 0; index1 < (CALIBRATION_NAMES_COUNTER); index1++)
	// debug_printf("%s %d coefs[%d] %f\n\r", __FILE__,
	// __LINE__,index1,coefs[index1]);

	if (err < 0)
	{
		debug_printf("%s %d Attention!!! Error while reading coefs\n\r",
					 __FILE__, __LINE__);
		debug_printf("!!!Stop!!!\n\r");
		while (1)
			;
	}

	debug_printf("crc: %#x\n", calibration_header.crc);
	debug_printf("date: %#x\n", calibration_header.date);
	debug_printf("time: %#x\n", calibration_header.time);
	debug_printf("git_commit: %#x\n", calibration_header.git_commit);
	debug_printf("from_display: %d\n", calibration_header.from_display);
	debug_printf("data_length: %d\n", calibration_header.data_length);
	uint32_t calibration_crc = crc32b(coefs, CALIBRATION_NAMES_COUNTER << 2);

	if (calibration_crc != calibration_header.crc)
	{
		debug_printf("%s %d Attention!!! Calibration CRC check failed\n\r"
					 "Calculated CRC:%#x\n\rCRC from file: %#x\n\r",
					 __FILE__, __LINE__, calibration_crc, calibration_header.crc);
		debug_printf("!!!Stop!!!\n\r");
		while (1);
	}
	else
	{
		debug_printf("CRC check OK\n\r");
	}

	// Чтение фильтров из ПЗУ.
	debug_printf("\n## Read filters\n");
	err = memory_read_settings_w_header(
		filters_addresses_lengths, 
		(void *)(FILTERS_SETT_ADDR),
		FILTERS_SETT_LENGTH << 2, 
		&filter_header
	);
	// for (index1 = 0; index1 < (FILTR_NAMES_COUNTER); index1++)
	// debug_printf("%s %d filtr[%d] %d\n\r", __FILE__,
	// __LINE__,index1,filtr_ld[index1]);
	if (err < 0)
	{
		debug_printf("%s %d Attention!!! Error while reading filtr_ld\n\r",
					 __FILE__, __LINE__);
		debug_printf("!!!Stop!!!\n\r");
		while (1);
	}

	debug_printf("crc: %#x\n\r", filter_header.crc);
	debug_printf("date: %#x\n\r", filter_header.date);
	debug_printf("time: %#x\n\r", filter_header.time);
	debug_printf("git_commit: %#x\n\r", filter_header.git_commit);
	debug_printf("from_display: %d\n\r", filter_header.from_display);
	debug_printf("data_length: %d\n\r", filter_header.data_length);
	uint32_t filter_crc =
		crc32b(filters_addresses_lengths, FILTERS_SETT_LENGTH << 2);

	if (filter_crc != filter_header.crc)
	{

		debug_printf("%s %d Attention!!! Filter CRC check failed.\n\r"
					 "Calculated CRC:%#x\n\rCRC from file: %#x\n\r",
					 __FILE__, __LINE__, filter_crc, filter_header.crc);
		debug_printf("!!!Stop!!!\n\r");
		while (1);
	}
	else
	{
		debug_printf("CRC check OK\n\r");
	}	

	


//****************************************************************************************************
// 	Читаем из flash структуру конфигурации системы см. файл highlvl/system_config.h
//****************************************************************************************************	
		
	err = memory_read_settings(&(main_config_file.config_struct), (void*)(SETTINGS_ADDR), sizeof(main_config_file.config_struct));
	if (err < 0)
	{
		debug_printf("%s %d Attention!!! Error while reading config_struct\n\r",
					 __FILE__, __LINE__);
		debug_printf("!!!Stop!!!\n\r");
		//while(1);
	}	
	
	param[NEUTRALMODE].value.val_int = main_config_file.config_struct.neutral_mode;

	set_MPORT_70_MHz();

	// Инициализация фильтров
	init_filters(filters_addresses_lengths);

	// Настройка периодических вызовов.
	static char name[] = "params";
	params_periodic.name = name;
	params_periodic.item = paritems;
	params_periodic.maxnum = CNT_PRM;
	params_periodic.call = params_periodic_call;
	err = periodic_init(&params_periodic);
	if (err < 0)
	{
		debug_printf("ERR! params_periodic\r");
	}

	// Настройка периодических вызовов для параметров источников
	static char name_A4[] = "params_A4";
	params_periodic_A4.name = name_A4;
	params_periodic_A4.item = paritems_A4;
	params_periodic_A4.maxnum = CNT_PRM;
	params_periodic_A4.call = params_periodic_call;
	err = periodic_init(&params_periodic_A4);
	if (err < 0)
	{
		debug_printf("ERR! params_periodic_A4\n\r");
	}

	static char name_A5[] = "params_A5";
	params_periodic_A5.name = name_A5;
	params_periodic_A5.item = paritems_A5;
	params_periodic_A5.maxnum = CNT_PRM;
	params_periodic_A5.call = params_periodic_call;
	err = periodic_init(&params_periodic_A5);
	if (err < 0)
	{
		debug_printf("ERR! params_periodic_A5\n\r");
	}

	static char name_A6[] = "params_A6";
	params_periodic_A6.name = name_A6;
	params_periodic_A6.item = paritems_A6;
	params_periodic_A6.maxnum = CNT_PRM;
	params_periodic_A6.call = params_periodic_call;
	err = periodic_init(&params_periodic_A6);
	if (err < 0)
	{
		debug_printf("ERR! params_periodic_A6\n\r");
	}

	// Инициализация параметров, поступающих по CAN из БУ СЭС и БУ 50 и из РЧВ
	init_extern_params();

	// Инициализация параметров Станции
	init_params_station();

	// Инициализация параметров Сети1
	init_params_net1();

	// Инициализация параметров ВИП2
	init_params_net2();

	// Инициализация параметров ЭА
	init_params_ea();

	// Инициализация параметров ЭН
	init_params_en();

	// Инициализация параметров УР400
	init_params_ur400();

	// Инициализация параметров УР230
	init_params_ur230();

	// Инициализация параметров УР27
	init_params_ur27();

	// Инициализация параметров НЗТ
	init_params_fuel_pump();

	// Инициализация параметров люков
	init_params_hatches();

	// Инициализация параметров ПЧ100
	init_params_fc1();

	// Инициализация параметров ПЧ100 2
	init_params_fc2();

	// Инициализация параметров БУ 50 - содержит инициализацию параметров
	// POLLING_MAV_Ax, поэтому делается в конце.
	init_params_bu();

} // End of init_params
//****************************************************************************************************
// Обновление параметров, принимаемых по CAN от БУ 400
/*
<field shift="0" size="1"   join="EA500_1" 	description="Напряжение ПЧ1 выше нормы"/>
<field shift="1" size="1"   join="EA501_1" 	description="Напряжение ПЧ1 ниже нормы"/>
<field shift="2" size="1"   join="EA502_1" 	description="Неверная фазировка сети 400 Гц"/>
<field shift="3" size="1"   join="EA503_1" 	description="Обрыв фаз сети 400 Гц"/>
<field shift="4" size="1"   join="EA507_1" 	description="Частота ПЧ1 ниже нормы"/>
<field shift="5" size="1"   join="EA508_1" 	description="Частота ПЧ1 выше нормы"/>
<field shift="6" size="1"   join="EA519_1" 	description="КЗ ПЧ1"/>
<field shift="7" size="1"   join="EA524" 	description="Нештатное отключение ПЧ"/>

<field shift="8" size="1"   join="EA554"	description="Неисправность контактора ПЧ"/>
<field shift="9" size="1"   join="EA555"	description="Неисправность контактора объединения шин ПЧ"/>
<field shift="10" size="1"  join="EA556"  	description="Неисправность контактора МКИ ПЧ"/>
<field shift="11" size="1"  join="EA557" 	description="Неисправность реле снятия возбуждения ПЧ"/>
<field shift="12" size="1"  join="EA558" 	description="Неисправность реле корректора ПЧ"/>
<field shift="13" size="1"  join="EA559" 	description="Неисправность реле самовозбуждения ПЧ"/>
<field shift="14" size="1"  join="EA560" 	description="Срабатывание МКИ ПЧ"/>
<field shift="15" size="1"  join="EA561" 	description="Отказ корректора возбуждения ПЧ"/>
*/
void can_bu_400_data_callback(void * arg,  intercom_can_pack_t * received_packet)
{
	
	uint32_t global_id	= ((uint32_t)(received_packet->data[3] << 24))
					| ((uint32_t)(received_packet->data[2] << 16))
					| ((uint32_t)(received_packet->data[1] << 8))
					| received_packet->data[0];
	uint32_t value 		= ((uint32_t)(received_packet->data[7] << 24))
					| ((uint32_t)(received_packet->data[6] << 16))
					| ((uint32_t)(received_packet->data[5] << 8))
					| received_packet->data[4];
					
	//debug_printf("global_id is %d, val is %d\r", global_id, val);
	switch (global_id)
	{
		// Частота ПЧ1
		case KEY_FC1_F_U_A:
		{
			// Записать в параметр
			param[FC1FUAEXT].value.val_int = value;
		}
		break;
		// Частота ПЧ2
		case KEY_FC2_F_U_A:
		{
			
			// Записать в параметр
			param[FC2FUAEXT].value.val_int = value;
		}
		break;
		case KEY_DISCRETES_400:
		{
			param[DISCRETES400].value.val_int = value;			
		}
		break;
		case KEY_DISCRETES2_400:
		{
			param[DISCRETES2400].value.val_int = value;	
		}
		break;
		case KEY_EVENTS_FC1_400:
		{
			if(value & (1<<0)) 	/*EA500_1*/ write_data_element(EA500_1, &switch_on, sizeof(switch_on));
			if(value & (1<<1)) 	/*EA501_1*/ write_data_element(EA501_1, &switch_on, sizeof(switch_on));
			if(value & (1<<2)) 	/*EA502_1*/ write_data_element(EA502_1, &switch_on, sizeof(switch_on));
			if(value & (1<<3)) 	/*EA503_1*/ write_data_element(EA503_1, &switch_on, sizeof(switch_on));
			if(value & (1<<4)) 	/*EA507_1*/ write_data_element(EA507_1, &switch_on, sizeof(switch_on));
			if(value & (1<<5)) 	/*EA508_1*/ write_data_element(EA508_1, &switch_on, sizeof(switch_on));
			if(value & (1<<6)) 	/*EA519_1*/ write_data_element(EA519_1, &switch_on, sizeof(switch_on));
			
			if(value & (1<<8)) 	/*EA554*/ 	write_data_element(EA554, 	&switch_on, sizeof(switch_on));
			if(value & (1<<9)) 	/*EA555*/ 	write_data_element(EA555, 	&switch_on, sizeof(switch_on));
			if(value & (1<<10))	/*EA556*/ 	write_data_element(EA556, 	&switch_on, sizeof(switch_on));
			if(value & (1<<11)) /*EA557*/ 	write_data_element(EA557, 	&switch_on, sizeof(switch_on));
			if(value & (1<<12)) /*EA558*/ 	write_data_element(EA558, 	&switch_on, sizeof(switch_on));
			if(value & (1<<13)) /*EA559*/ 	write_data_element(EA559, 	&switch_on, sizeof(switch_on));
			if(value & (1<<14)) /*EA560*/ 	write_data_element(EA560, 	&switch_on, sizeof(switch_on));
			if(value & (1<<15)) /*EA561*/ 	write_data_element(EA561, 	&switch_on,	sizeof(switch_on));
		}
		break;
        case KEY_EVENTS_FC2_400:
		{
			if(value & (1<<0)) 	/*EA500_2*/ write_data_element(EA500_2, &switch_on, sizeof(switch_on));
			if(value & (1<<1)) 	/*EA501_2*/ write_data_element(EA501_2, &switch_on, sizeof(switch_on));
			if(value & (1<<2)) 	/*EA502_2*/ write_data_element(EA502_2, &switch_on, sizeof(switch_on));
			if(value & (1<<3)) 	/*EA503_2*/ write_data_element(EA503_2, &switch_on, sizeof(switch_on));
			if(value & (1<<4)) 	/*EA507_2*/ write_data_element(EA507_2, &switch_on, sizeof(switch_on));
			if(value & (1<<5)) 	/*EA508_2*/ write_data_element(EA508_2, &switch_on, sizeof(switch_on));
			if(value & (1<<6)) 	/*EA519_2*/ write_data_element(EA519_2, &switch_on, sizeof(switch_on));
			
			if(value & (1<<8)) 	/*EA554_2*/ 	write_data_element(EA554_2, 	&switch_on, sizeof(switch_on));
			if(value & (1<<9)) 	/*EA555_2*/ 	write_data_element(EA555_2, 	&switch_on, sizeof(switch_on));
			if(value & (1<<10))	/*EA556_2*/ 	write_data_element(EA556_2, 	&switch_on, sizeof(switch_on));
			if(value & (1<<11)) /*EA557_2*/ 	write_data_element(EA557_2, 	&switch_on, sizeof(switch_on));
			if(value & (1<<12)) /*EA558_2*/ 	write_data_element(EA558_2, 	&switch_on, sizeof(switch_on));
			if(value & (1<<13)) /*EA559_2*/ 	write_data_element(EA559_2, 	&switch_on, sizeof(switch_on));
			if(value & (1<<14)) /*EA560_2*/ 	write_data_element(EA560_2, 	&switch_on, sizeof(switch_on));
			if(value & (1<<15)) /*EA561_2*/ 	write_data_element(EA561_2, 	&switch_on,	sizeof(switch_on));
		}
		break;
        // Выбран бак 
        case NZT_SELECTED_TANK:
        {
            param[NZTSELECTEDTANK].value.val_int = value;
        }
        break;
        
		// Прочие параметры БУ 50 не нужны. Оставлено на всякий случай.
		default:
		{;}
		break;
	}
}// End of update_params_from_BU_400

void print_me ()
{
	unsigned char n;
	task_t *t;

	task_print (&debug, 0);
		n = 0;
		list_iterate (t, &task_active) {
			if (t != task_idle && t != task_current)
				task_print (&debug, t);
			if (! uos_valid_memory_address (t))
				break;
			if (++n > 32 || list_is_empty (&t->item)) {
				debug_puts ("...\n");
				break;
			}
		}
		if (task_current && task_current != task_idle)
			task_print (&debug, task_current);

		debug_dump_stack (task_name (task_current), __builtin_alloca (0),
			(void*) task_current->stack_context, __builtin_return_address (0));


}

//****************************************************************************************************
// Обновление параметров, принимаемых по CAN от БУ СЭС (sources CAN ID = 47)
//					<field shift="0" size="1" join="EA301" 	    description="Пожар"/>
//					<field shift="7" size="1" join="EA321" 		description="Низкое напряжение АКБ ХД"/>
//					<field shift="8" size="1" join="EA323"		description="Низкое напряжение АКБ (СТ/ОП)"/>
//					<field shift="16" size="1" join="EA300" 	description="Аварийный останов"/>

void can_bu_ses_data_callback(void * arg,  intercom_can_pack_t * received_packet)
{
	static uint32_t prev_value_v = 0;
	
	uint32_t global_id 	= (	(uint32_t)(received_packet->data[3] << 24))
							| ((uint32_t)(received_packet->data[2] << 16))
							| ((uint32_t)(received_packet->data[1] << 8))
							| received_packet->data[0];
	uint32_t value_v 		= (	(uint32_t)(received_packet->data[7] << 24))
							| ((uint32_t)(received_packet->data[6] << 16))
							| ((uint32_t)(received_packet->data[5] << 8))
							| received_packet->data[4];
	switch (global_id)
	{

		case KEY_STATION_CONTROL_MODE:
		{
			write_data_element(STATION_CONTROL_MODE, &value_v, sizeof(value_v));
		}break;
		
		case KEY_EVENTS_BLOCK:
		{
		    //Поставил принтфы для того, чтобы понять почему в случайный момент времени 
            //срабатывают данные аварии
			
			// временный костыль. авария срабатывает только если два раза подряд пришло одно и то же число
        if (value_v == prev_value_v)
        {    
            if(value_v & (1<<0))
            {   
                 debug_printf("%s %d value_v %d\n\r",__FILE__,__LINE__,value_v);
				 print_me ();
                /*EA301*/ write_data_element(EA301, &switch_on, sizeof(switch_on));
            }	
            if(value_v & (1<<3)) 	/*EA354*/ write_data_element(EA354, &switch_on, sizeof(switch_on));
			if(value_v & (1<<4)) 	/*EA355*/ write_data_element(EA355, &switch_on, sizeof(switch_on));
			if(value_v & (1<<7)) 	
            { 
                 debug_printf("%s %d value_v %d\n\r",__FILE__,__LINE__,value_v);
				 print_me ();
                /*EA321*/ write_data_element(EA321, &switch_on, sizeof(switch_on));
            }	
            if(value_v & (1<<8)) 	/*EA323*/ write_data_element(EA323, &switch_on, sizeof(switch_on));
			if(value_v & (1<<16))	
            { 
                 debug_printf("%s %d value_v %d\n\r",__FILE__,__LINE__,value_v);
				 print_me ();
                /*EA300*/ write_data_element(EA300, &switch_on, sizeof(switch_on));
            }	
			if(value_v & (1<<29)) 	/*EA601*/ write_data_element(EA601, &switch_on, sizeof(switch_on));		
			if(value_v & (1<<30)) 	/*EP602*/ write_data_element(EP602, &switch_on, sizeof(switch_on));		
			if(value_v & (1<<31)) 	/*EA352*/ write_data_element(EA352, &switch_on, sizeof(switch_on));		
        }
		prev_value_v = value_v;    
        }break;	
		
		case KEY_DISCRETES2_SES:
		{
			write_data_element(DISCRETES2_SES, &value_v, sizeof(value_v));
		}break;
		case KEY_NZT_SELECTED_TANK:
		{
			write_data_element(NZT_SELECTED_TANK, &value_v, sizeof(value_v));
		}break;
		case KEY_PDU_COMMAND:
		{
			write_data_element(PDU_COMMAND, &value_v, sizeof(value_v));
		}break;
		case KEY_AIR_TEMP:
		{
			write_data_element(AIR_TEMP, &value_v, sizeof(value_v));
		}break;
		
		// Прочие параметры БУ СВЭП не нужны. Оставлено на всякий случай.
		default:
		{if(global_id != 12106) debug_printf("%s %d wrong global id%d\n\r",__FILE__,__LINE__,global_id);}
		break;
	}//case						
}//can_bu_ses_data_callback

