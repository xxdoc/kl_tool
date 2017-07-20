function [cid,nr,centers] = kkm(x,k,nc)
%KKM Summary of this function goes here
%     BasicKMeans.m主类 
[n,d,z] = size(x);
% 设置cid为分类结果显示矩阵
cid = zeros(1,n); 
% Make this different to get the loop started.
oldcid = ones(1,n);
% The number in each cluster.
nr = zeros(1,k); 
% Set up maximum number of iterations.
maxgn= 100;
iter = 1;
while iter < maxgn
%计算每个数据到聚类中心的距离
    for i = 1:n
      dist = sum( (repmat(x(i,:),k,1) - nc ).^2, 2);
      [m,ind] = min(dist); % 将当前聚类结果存入cid中
      cid(i) = ind;
    end

    for i = 1:k
    %找到每一类的所有数据，计算他们的平均值，作为下次计算的聚类中心
      ind = find(cid==i);
      nc(i,:) = mean(x(ind,:));
      % 统计每一类的数据个数
      nr(i) = length(ind);
    end

    iter = iter + 1;
end

% Now check each observation to see if the error can be minimized some more. 
% Loop through all points.
maxiter = 2;
iter = 1;
move = 1;
while (iter < maxiter) && ( move ~= 0 )
    move = 0;

% 对所有的数据进行再次判断，寻求最佳聚类结果
for i = 1:n
  dist = sum((repmat(x(i,:),k,1)-nc).^2,2);
  r = cid(i);  % 将当前数据属于的类给r
  dadj = nr./(nr+1).*dist'; % 计算调整后的距离
  [m,ind] = min(dadj); % 找到该数据距哪个聚类中心最近
  if ind ~= r  % 如果不等则聚类中心移动
   cid(i) = ind;%将新的聚类结果送给cid
   ic = find(cid == ind);%重新计算调整当前类别的聚类中心
   nc(ind,:) = mean(x(ic,:));
   move = 1;
  end
end
iter = iter+1;
end
centers = nc;


if move == 0
    disp('No points were moved after the initial clustering procedure.')
else
    disp('Some points were moved after the initial clustering procedure.')
end 

end

