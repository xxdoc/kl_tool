#!/usr/bin/env python
# -*- coding:utf-8 -*-
##***********************************
##**********class AiSnake************
##***********************************

class AiSnake(object):

    def __init__(self, _width, _height):
        self.width = _width
        self.height = _height

        self.field_size = self.height * self.width
        self.left = -1
        self.right = 1
        self.up = -self.width
        self.down = self.width
        self.mov = [self.left, self.right, self.up, self.down]

    def log(self, msg):
        if getattr(self, 'log_file', None):
            self.log_file.write(msg)
            self.log_file.flush()

    def log_dist(self, dist, snake, dest):
        if getattr(self, 'log_file', None):
            msg = self.dist2str(dist, snake, dest)
            self.log(msg)

    def dist2str(self, dist, snake, dest):
        tmp = []
        msg = "try goto:%d x:%d y:%d\n" % (dest, dest%self.width, dest/self.width)
        for i in xrange(self.height):
            for j in xrange(self.width):
                if i*self.width+j == snake[0]:
                    tmp.append("  A")
                elif len(snake) > 1 and i*self.width+j == snake[1]:
                    tmp.append("  B")
                elif len(snake) > 2 and i*self.width+j == snake[2]:
                    tmp.append("  C")
                elif i*self.width+j == snake[len(snake)-3]:
                    tmp.append("  X")
                elif i*self.width+j == snake[len(snake)-2]:
                    tmp.append("  Y")
                elif i*self.width+j == snake[len(snake)-1]:
                    tmp.append("  Z")
                else:
                    tmp.append("%3d"%(dist[i*self.width+j],))
            tmp.append('\n')
        tmp.append('\n')
        return msg + ''.join(tmp)

    def find_move(self, wormCoods, apple):
        food = apple[1] * self.width + apple[0]
        snake = [point[1] * self.width + point[0] for point in wormCoods]
        tmp = self.ai_move(snake, food)
        cmd = ('left', 'right', 'up', 'down')
        for i,t in enumerate(self.mov):
            if tmp==t:
                return cmd[i]
        return None

    def get_dist(self, snake, dest):
        queue = [dest, ]
        dist = [-2 for i in range(self.field_size)]
        for idx in snake:
            dist[idx] = -1
        dist[dest] = 0

        ret = False
        while queue:
            idx = queue.pop(0)
            for item in self.mov:
                if self.is_out_border(idx, item):
                    continue
                _idx = idx + item
                if _idx == snake[0]:
                    ret = True
                if dist[_idx] == -2:
                    dist[_idx] = dist[idx] + 1
                    queue.append(_idx)

        return dist, ret

    def mov_for_tail(self, snake, use_last):
        dist, found = self.get_dist(snake[:-1], snake[-1])
        if found:
            self.log_dist(dist, snake, snake[-1])
            ret = self._find_ret_dist(snake[0], dist)
            return self._find_ret_move(ret, snake[0]-snake[1], max, use_last)

        return None, None

    def mov_for_food(self, snake, food, use_last):
        dist, found = self.get_dist(snake, food)
        if found:
            self.log_dist(dist, snake, food)
            ret = self._find_ret_dist(snake[0], dist)
            while ret:
                tmp, min_val = self._find_ret_move(ret, snake[0]-snake[1], min, use_last)
                if not tmp:
                    break

                ret.pop(tmp)
                snake_tmp= snake[:]
                snake_tmp.insert(0, snake[0] + tmp)
                snake_tmp = snake_tmp if snake_tmp[0]==food else snake_tmp[:-1]
                can_tail, max_tail = self.mov_for_tail(snake_tmp, use_last)
                if can_tail:
                    return tmp, min_val

        return None, None

    def ai_move(self, snake, food):
        harflen = min(self.height, self.width) / 2 + 1
        slen = len(snake) * 1.0
        harf_move = max(0, (1 - slen/self.field_size)*harflen-1)
        is_find_food = slen < self.field_size*0.7

        goto_food, min_val = self.mov_for_food(snake, food, True)
        if goto_food and (is_find_food or min_val==0) and (slen<self.field_size*0.3 or min_val<=harf_move) :
        	    return goto_food

        follow_tail, max_tail = self.mov_for_tail(snake, is_find_food)
        if follow_tail:
            return follow_tail

        raise RuntimeError('Cannot find best move!')

    def _find_ret_dist(self, head, dist):
        dist_len = len(dist)
        ret = {item:dist[head+item] for item in self.mov if head+item<dist_len \
                                and not self.is_out_border(head, item) and dist[head+item] >= 0}
        return ret

    @staticmethod
    def _find_ret_move(ret, last, max_min, use_last=True):
        if not ret:
            return None

        max_val = max_min(ret.values())
        if ret.get(last, None)==max_val and use_last:
            return last, max_val
        else:
            for k, v in ret.items():
                if v==max_val:
                    return k, max_val

    def is_out_border(self, pos, move):
        if move == self.right and pos % self.width == self.width - 1:
            return True
        elif move == self.left and pos % self.width == 0:
            return True
        elif move == self.down and pos / self.width == self.height - 1:
            return True
        elif move == self.up and pos / self.width == 0:
            return True
        return False

def main():
    pass

if __name__ == '__main__':
    main()