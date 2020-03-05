-- select * from D_MAIN_MENUS connect by prior id = pid start with pid is null
-- select x, y, z from D_MAIN_MENUS connect by prior id = pid start with pid is null
-- select t.x as xx, y, z from D_MAIN_MENUS t connect by prior id = pid start with pid is null
select t.x as xx, t.y, t.z from D_MAIN_MENUS t connect by prior t.id = t.pid start with t.pid is null