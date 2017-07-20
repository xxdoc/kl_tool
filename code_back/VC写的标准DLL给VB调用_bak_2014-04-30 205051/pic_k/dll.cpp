#include "dll.h"

BOOL APIENTRY DllMain( HANDLE hModule, 
                       DWORD  ul_reason_for_call, 
                       LPVOID lpReserved
					 )
{
    switch (ul_reason_for_call)
	{
		case DLL_PROCESS_ATTACH:
		case DLL_THREAD_ATTACH:
		case DLL_THREAD_DETACH:
		case DLL_PROCESS_DETACH:
			break;
    }
    return TRUE;
}

#define DLL_VER_CODE 0x01f0f00f
#define DLL_OK_CODE 0
#define DLL_ERROR_CODE -1

#define DLL_MAX_BUFFER_SIZE 8192

/*** DLL SET START  ***/

long _C_ TEST_DLL(long s1, long s2) {
	return s1 + s2;
}

long _C_ GET_DLL_VER_CODE() {
	return DLL_VER_CODE;
}

long _C_ GET_DLL_OK_CODE() {
	return DLL_OK_CODE;
}

long _C_ GET_DLL_ERROR_CODE() {
	return DLL_ERROR_CODE;
}

long _C_ GET_DLL_MAX_BUFFER_SIZE() {
	return DLL_MAX_BUFFER_SIZE;
}

/*** DLL SET END  ***/
/*** public function start ***/

char gobal_buffer[DLL_MAX_BUFFER_SIZE];

long my_strlen(LPSTR str);
void my_strcpy(LPSTR from, LPSTR to);


long _C_ setStr(LPSTR str) {
    if (my_strlen(str) < DLL_MAX_BUFFER_SIZE - 1 )
	{
		my_strcpy(gobal_buffer, str);
		return DLL_OK_CODE;
	}
	else
		return DLL_ERROR_CODE;
}

long _C_ getStr(LPSTR out) {
	my_strcpy(out, gobal_buffer);
	return DLL_OK_CODE;
}

long _C_ getLen() {
	return my_strlen(gobal_buffer);
}


long _C_ pic_set_piex(unsigned char * rgb_buff, long pic_height, long pic_width, long row_width, long v_split,long v_range, long v_set) {
	unsigned char v_comp[3]={0};
	unsigned char comp[2][3]={0};
	unsigned char temp_color;
	int loop_i, loop_j, temp_index;

	v_comp[0] = (unsigned char)(v_split / 65536);
	v_comp[1] = (unsigned char)( (v_split % 65536) / 256 );
	v_comp[2] = (unsigned char)(v_split % 256);
	for(loop_i = 0;loop_i <= 2; loop_i++){
		comp[0][loop_i] = (unsigned char)(v_comp[loop_i] - v_range);
		comp[1][loop_i] = (unsigned char)(v_comp[loop_i] + v_range);
	}

	temp_color = (unsigned char)v_set;
	for(loop_i = 0;loop_i < pic_height; loop_i++){
		for(loop_j = 0;loop_j < pic_width; loop_j++){
			temp_index = loop_i*row_width + loop_j;
			if( (rgb_buff[temp_index] < comp[0][0]) && (rgb_buff[temp_index+1] < comp[0][1]) && (rgb_buff[temp_index+2] < comp[0][2]) && 
				(rgb_buff[temp_index] < comp[1][0]) && (rgb_buff[temp_index+1] < comp[1][1]) && (rgb_buff[temp_index+2] < comp[1][2]) ) {
				rgb_buff[temp_index] = temp_color;
				rgb_buff[temp_index+1] = temp_color;
				rgb_buff[temp_index+2] = temp_color;
			}
		}
	}

	return 0;
}

long _C_ pic_to_gray(unsigned char * rgb_buff, long pic_height, long pic_width, long row_width) {
	unsigned char temp_color;
	int loop_i, loop_j, temp_index;

	for(loop_i = 0;loop_i < pic_height; loop_i++){
		for(loop_j = 0;loop_j < pic_width; loop_j++){
			temp_index = loop_i*row_width + loop_j;
			temp_color = ( (rgb_buff[temp_index] + 1) / 3 ) + ( rgb_buff[temp_index + 1] / 3 ) + ( rgb_buff[temp_index + 2] / 3 );
			rgb_buff[temp_index] = temp_color;
			rgb_buff[temp_index+1] = temp_color;
			rgb_buff[temp_index+2] = temp_color;
		}
	}

	return 0;
} 

long _C_ pic_to_block(unsigned char * rgb_buff, long pic_height, long pic_width, long row_width, long v_block_sqrt, long v_block_index) {
	unsigned char temp_color;
	int loop_i, loop_j,loop_k, loop_l, temp_index, temp_height, temp_width;

	temp_height = pic_height / v_block_sqrt;
	temp_width = pic_width / v_block_sqrt;
	for(loop_i = 0;loop_i <= temp_height; loop_i += v_block_sqrt){
		for(loop_j = 0;loop_j <= temp_width; loop_j += v_block_sqrt){
			temp_index = loop_i * row_width + loop_j;

			temp_color = rgb_buff[temp_index + row_width*( v_block_index%( (v_block_sqrt*v_block_sqrt) / v_block_sqrt) ) + (v_block_index % v_block_sqrt)];
			for(loop_k = 0;loop_k < v_block_sqrt; loop_k ++) {
				for(loop_l = 0;loop_l < v_block_sqrt; loop_l ++) {
					temp_index += loop_k * row_width + loop_l;
					rgb_buff[temp_index] = temp_color;
					rgb_buff[temp_index+1] = temp_color;
					rgb_buff[temp_index+2] = temp_color;
				}
			}
		}
		//do the end of each row   pic_width / v_block_sqrt
		temp_width = pic_width % v_block_sqrt;
		for(loop_j = 0;loop_j <= temp_width; loop_j ++){
			temp_index = loop_i * row_width + loop_j + pic_width / v_block_sqrt;

			temp_color = rgb_buff[temp_index + row_width*( v_block_index%( (v_block_sqrt*v_block_sqrt) / temp_width) ) + (v_block_index % temp_width)];
			for(loop_k = 0;loop_k < v_block_sqrt; loop_k ++) {
				for(loop_l = 0;loop_l <= temp_width; loop_l ++) {
					temp_index += loop_k * row_width + loop_l;
					rgb_buff[temp_index] = temp_color;
					rgb_buff[temp_index+1] = temp_color;
					rgb_buff[temp_index+2] = temp_color;
				}
			}
		}
	} 
	//do the last row that less  pic_height / v_block_sqrt
	temp_height = pic_height % v_block_sqrt;
	temp_width = pic_width / v_block_sqrt;
	for(loop_i = 0;loop_i <= temp_height; loop_i += v_block_sqrt){
		for(loop_j = 0;loop_j <= temp_width; loop_j += v_block_sqrt){
			temp_index = loop_i * row_width + loop_j + pic_height / v_block_sqrt;

			temp_color = rgb_buff[temp_index + row_width*( v_block_index%( (v_block_sqrt*v_block_sqrt) / v_block_sqrt) ) + (v_block_index % v_block_sqrt)];
			for(loop_k = 0;loop_k <= temp_height; loop_k ++) {
				for(loop_l = 0;loop_l < v_block_sqrt; loop_l ++) {
					temp_index += loop_k * row_width + loop_l;
					rgb_buff[temp_index] = temp_color;
					rgb_buff[temp_index+1] = temp_color;
					rgb_buff[temp_index+2] = temp_color;
				}
			}
		}
		//do the end of the  last row that less  pic_height / v_block_sqrt and   pic_width / v_block_sqrt
		temp_width = pic_width % v_block_sqrt;
		for(loop_j = 0;loop_j <= temp_width; loop_j ++){
			temp_index = loop_i * row_width + loop_j + pic_height / v_block_sqrt + pic_width / v_block_sqrt;

			temp_color = rgb_buff[temp_index + row_width*( v_block_index%( (temp_height*temp_height) / temp_width) ) + (v_block_index % temp_width)];
			for(loop_k = 0;loop_k <= temp_height; loop_k ++) {
				for(loop_l = 0;loop_l <= temp_width; loop_l ++) {
					temp_index += loop_k * row_width + loop_l;
					rgb_buff[temp_index] = temp_color;
					rgb_buff[temp_index+1] = temp_color;
					rgb_buff[temp_index+2] = temp_color;
				}
			}
		}
	}

	return 0;
} 


long _C_ pic_to_block_out(unsigned char * rgb_buff, long pic_height, long pic_width, long row_width, long v_block_sqrt, long v_block_index, unsigned char * out_buff) {
	unsigned char temp_color;
	int loop_i, loop_j, temp_index, temp_height, temp_width;
	long temp_out_row_width, temp_out_index;

	temp_out_row_width = ( (pic_width / v_block_sqrt) + (pic_width / v_block_sqrt) % 4 ) / 4;

	temp_height = pic_height / v_block_sqrt;
	temp_width = pic_width / v_block_sqrt;
	for(loop_i = 0;loop_i <= temp_height; loop_i += v_block_sqrt){
		for(loop_j = 0;loop_j <= temp_width; loop_j += v_block_sqrt){
			temp_index = loop_i * row_width + loop_j;
			temp_color = rgb_buff[temp_index + row_width*( v_block_index%( (v_block_sqrt*v_block_sqrt) / v_block_sqrt) ) + (v_block_index % v_block_sqrt)];
			temp_out_index = temp_height * temp_out_row_width + temp_width;
			out_buff[temp_out_index] = temp_color;
		}
	} 
	
	return 0;
} 


long _C_ pic_to_split_rgb(unsigned char * rgb_buff, long pic_height, long pic_width, long row_width, long v_split) {
	unsigned char v_comp[3]={0};
	int loop_i, loop_j, temp_index;

	v_comp[0] = (unsigned char)(v_split / 65536);
	v_comp[1] = (unsigned char)( (v_split % 65536) / 256 );
	v_comp[2] = (unsigned char)(v_split % 256);

	for(loop_i = 0;loop_i < pic_height; loop_i++){
		for(loop_j = 0;loop_j < pic_width; loop_j++){
			temp_index = loop_i*row_width + loop_j;
			if( (rgb_buff[temp_index] < v_comp[0]) && (rgb_buff[temp_index+1] < v_comp[1]) && (rgb_buff[temp_index+2] < v_comp[2]) ) {
				rgb_buff[temp_index] = 0;
				rgb_buff[temp_index+1] = 0;
				rgb_buff[temp_index+2] = 0;
			} else {
				rgb_buff[temp_index] = 255;
				rgb_buff[temp_index+1] = 255;
				rgb_buff[temp_index+2] = 255;
			}
		}
	}

	return 0;
}

long _C_ pic_to_split_gray(unsigned char * rgb_buff, long pic_height, long pic_width, long row_width, long v_split) {
	unsigned char temp_color;
	int loop_i, loop_j, temp_index;


	temp_color = (unsigned char)v_split;
	for(loop_i = 0;loop_i < pic_height; loop_i++){
		for(loop_j = 0;loop_j < pic_width; loop_j++){
			temp_index = loop_i*row_width + loop_j;
			if( (rgb_buff[temp_index] < temp_color) && (rgb_buff[temp_index+1] < temp_color) && (rgb_buff[temp_index+2] < temp_color) ) {
				rgb_buff[temp_index] = 0;
				rgb_buff[temp_index+1] = 0;
				rgb_buff[temp_index+2] = 0;
			} else {
				rgb_buff[temp_index] = 255;
				rgb_buff[temp_index+1] = 255;
				rgb_buff[temp_index+2] = 255;
			}
		}
	}

	return 0;
}

/*** private function start ***/

long my_strlen(LPSTR str) {
	if(str == NULL)
		return 0; 
	long len = 0; 
	while((*str++) != '\0')
		len++; 
	return len; 
}

void my_strcpy(LPSTR strDest, LPSTR strSrc){
	char * strDestCopy = strDest;
	if ((NULL==strDest)||(NULL==strSrc))
		return;
	while(*strDest++=*strSrc++);
}
